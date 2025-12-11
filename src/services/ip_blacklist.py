"""
IP Blacklist Service
Tracks IP addresses that violate rate limits and blocks them after X violations.
"""
import os
import time
from collections import defaultdict
from typing import Dict, Set

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class IPBlacklist:
    """
    IP Blacklist service.
    Tracks violations per IP and blocks after threshold.
    """
    
    # Configuration
    VIOLATIONS_THRESHOLD = int(os.getenv("IP_BLACKLIST_THRESHOLD", "10"))  # Block after 10 violations
    BLACKLIST_DURATION_SECONDS = int(os.getenv("IP_BLACKLIST_DURATION", "3600"))  # 1 hour default
    
    def __init__(self):
        self.redis_client = None
        self.violations: Dict[str, int] = defaultdict(int)  # IP -> violation count
        self.blacklisted: Set[str] = set()  # IP -> blacklisted until timestamp
        
        # Try Redis
        redis_url = os.getenv("REDIS_URL")
        if redis_url and REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                )
                self.redis_client.ping()
                print("✅ IP Blacklist using Redis")
            except Exception as e:
                print(f"⚠️  Redis unavailable for blacklist, using in-memory: {e}")
                self.redis_client = None
    
    def record_violation(self, ip_address: str):
        """Record a rate limit violation for IP"""
        if self.redis_client:
            try:
                key = f"blacklist:violations:{ip_address}"
                violations = self.redis_client.incr(key)
                self.redis_client.expire(key, 3600)  # Expire after 1 hour
                
                if violations >= self.VIOLATIONS_THRESHOLD:
                    # Add to blacklist
                    blacklist_key = f"blacklist:blocked:{ip_address}"
                    self.redis_client.setex(
                        blacklist_key,
                        self.BLACKLIST_DURATION_SECONDS,
                        str(int(time.time()))
                    )
                    print(f"🚫 IP {ip_address} blacklisted after {violations} violations")
            except Exception:
                pass  # Fall through to in-memory
        else:
            # In-memory
            self.violations[ip_address] += 1
            
            if self.violations[ip_address] >= self.VIOLATIONS_THRESHOLD:
                self.blacklisted.add(ip_address)
                print(f"🚫 IP {ip_address} blacklisted after {self.violations[ip_address]} violations")
    
    def is_blacklisted(self, ip_address: str) -> bool:
        """Check if IP is blacklisted"""
        if self.redis_client:
            try:
                blacklist_key = f"blacklist:blocked:{ip_address}"
                return self.redis_client.exists(blacklist_key) > 0
            except Exception:
                return ip_address in self.blacklisted
        else:
            return ip_address in self.blacklisted
    
    def clear_violations(self, ip_address: str):
        """Clear violations for IP (e.g., after manual review)"""
        if self.redis_client:
            try:
                self.redis_client.delete(f"blacklist:violations:{ip_address}")
                self.redis_client.delete(f"blacklist:blocked:{ip_address}")
            except Exception:
                pass
        
        self.violations.pop(ip_address, None)
        self.blacklisted.discard(ip_address)
    
    def get_violations(self, ip_address: str) -> int:
        """Get violation count for IP"""
        if self.redis_client:
            try:
                key = f"blacklist:violations:{ip_address}"
                return int(self.redis_client.get(key) or 0)
            except Exception:
                return self.violations.get(ip_address, 0)
        else:
            return self.violations.get(ip_address, 0)


# Global instance
ip_blacklist = IPBlacklist()

