#!/usr/bin/env python3
# type: ignore
"""
Automated CHANGELOG Generator
Generates changelog from conventional commits
"""
import subprocess
import re
from datetime import datetime
from collections import defaultdict
import sys

# Conventional commit types
COMMIT_TYPES = {
    'feat': {'title': '✨ Features', 'emoji': '✨'},
    'fix': {'title': '🐛 Bug Fixes', 'emoji': '🐛'},
    'docs': {'title': '📚 Documentation', 'emoji': '📚'},
    'style': {'title': '💄 Styling', 'emoji': '💄'},
    'refactor': {'title': '♻️ Code Refactoring', 'emoji': '♻️'},
    'perf': {'title': '⚡ Performance', 'emoji': '⚡'},
    'test': {'title': '✅ Tests', 'emoji': '✅'},
    'build': {'title': '🏗️ Build System', 'emoji': '🏗️'},
    'ci': {'title': '👷 CI/CD', 'emoji': '👷'},
    'chore': {'title': '🔧 Chores', 'emoji': '🔧'},
    'revert': {'title': '⏪ Reverts', 'emoji': '⏪'},
}

def get_git_tags():
    """Get all git tags sorted by date"""
    try:
        result = subprocess.run(
            ['git', 'tag', '--sort=-creatordate'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []

def get_commits_since(since_ref=None):
    """Get commits since a specific ref (tag or commit)"""
    cmd = ['git', 'log', '--pretty=format:%H|%s|%b|%an|%ae|%ad', '--date=short']
    
    if since_ref:
        cmd.append(f'{since_ref}..HEAD')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []

def parse_commit(commit_line):
    """Parse a commit line into structured data"""
    parts = commit_line.split('|')
    if len(parts) < 6:
        return None
    
    hash, subject, body, author, email, date = parts[:6]
    
    # Parse conventional commit format: type(scope): subject
    match = re.match(r'^(\w+)(?:\(([^)]+)\))?:\s*(.+)$', subject)
    
    if not match:
        return {
            'hash': hash[:7],
            'type': 'other',
            'scope': None,
            'subject': subject,
            'body': body,
            'author': author,
            'email': email,
            'date': date,
            'breaking': 'BREAKING CHANGE' in body
        }
    
    commit_type, scope, message = match.groups()
    
    return {
        'hash': hash[:7],
        'type': commit_type.lower(),
        'scope': scope,
        'subject': message,
        'body': body,
        'author': author,
        'email': email,
        'date': date,
        'breaking': 'BREAKING CHANGE' in body or '!' in subject
    }

def generate_changelog_section(commits, version=None):
    """Generate changelog section for a version"""
    if not commits:
        return ""
    
    # Group commits by type
    grouped = defaultdict(list)
    breaking_changes = []
    
    for commit in commits:
        if commit['breaking']:
            breaking_changes.append(commit)
        
        commit_type = commit['type']
        if commit_type in COMMIT_TYPES:
            grouped[commit_type].append(commit)
        else:
            grouped['other'].append(commit)
    
    # Generate markdown
    lines = []
    
    # Version header
    if version:
        lines.append(f"\n## [{version}] - {datetime.now().strftime('%Y-%m-%d')}")
    else:
        lines.append(f"\n## [Unreleased] - {datetime.now().strftime('%Y-%m-%d')}")
    
    lines.append("")
    
    # Breaking changes first
    if breaking_changes:
        lines.append("### ⚠️ BREAKING CHANGES")
        lines.append("")
        for commit in breaking_changes:
            scope_str = f"**{commit['scope']}**: " if commit['scope'] else ""
            lines.append(f"- {scope_str}{commit['subject']} ([{commit['hash']}](../../commit/{commit['hash']}))")
        lines.append("")
    
    # Group by type
    for commit_type in ['feat', 'fix', 'docs', 'perf', 'refactor', 'style', 'test', 'build', 'ci', 'chore']:
        if commit_type not in grouped:
            continue
        
        type_info = COMMIT_TYPES.get(commit_type, {'title': commit_type.title(), 'emoji': ''})
        lines.append(f"### {type_info['title']}")
        lines.append("")
        
        for commit in grouped[commit_type]:
            scope_str = f"**{commit['scope']}**: " if commit['scope'] else ""
            lines.append(f"- {scope_str}{commit['subject']} ([{commit['hash']}](../../commit/{commit['hash']}))")
        
        lines.append("")
    
    # Other commits
    if 'other' in grouped and grouped['other']:
        lines.append("### 📝 Other Changes")
        lines.append("")
        for commit in grouped['other']:
            lines.append(f"- {commit['subject']} ([{commit['hash']}](../../commit/{commit['hash']}))")
        lines.append("")
    
    return '\n'.join(lines)

def generate_full_changelog():
    """Generate complete changelog from all tags"""
    tags = get_git_tags()
    
    # Start with header
    changelog = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

"""
    
    # Unreleased changes
    if tags:
        commits = get_commits_since(tags[0])
    else:
        commits = get_commits_since()
    
    if commits:
        parsed_commits = [parse_commit(c) for c in commits if c]
        parsed_commits = [c for c in parsed_commits if c]
        changelog += generate_changelog_section(parsed_commits)
    
    # Released versions
    for i, tag in enumerate(tags):
        since_ref = tags[i + 1] if i + 1 < len(tags) else None
        
        if since_ref:
            commits = get_commits_since(f'{since_ref}..{tag}')
        else:
            commits = get_commits_since(f'..{tag}')
        
        if commits:
            parsed_commits = [parse_commit(c) for c in commits if c]
            parsed_commits = [c for c in parsed_commits if c]
            changelog += generate_changelog_section(parsed_commits, version=tag)
    
    return changelog

def main():
    """Main function"""
    print("📝 Generating CHANGELOG.md...")
    
    changelog = generate_full_changelog()
    
    # Write to file
    with open('CHANGELOG.md', 'w') as f:
        f.write(changelog)
    
    print("✅ CHANGELOG.md generated successfully!")
    print(f"📄 {len(changelog.split(chr(10)))} lines written")

if __name__ == '__main__':
    main()
