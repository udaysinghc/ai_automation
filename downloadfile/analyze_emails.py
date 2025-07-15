#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from collections import Counter
import re

def load_email_data(file_path):
    """Load email data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"results": [], "count": 0}

def categorize_email_type(sender, subject, snippet):
    """Categorize email type based on sender, subject, and content"""
    sender_lower = sender.lower()
    subject_lower = subject.lower()
    snippet_lower = snippet.lower()
    
    # Newsletter/Marketing indicators
    newsletter_keywords = ['newsletter', 'unsubscribe', 'marketing', 'promotion', 'deal', 'offer']
    if any(keyword in snippet_lower or keyword in subject_lower for keyword in newsletter_keywords):
        return 'Newsletter/Marketing'
    
    # Automated/System emails
    system_keywords = ['no-reply', 'noreply', 'automated', 'system', 'notification']
    if any(keyword in sender_lower for keyword in system_keywords):
        return 'System/Automated'
    
    # Work-related domains and keywords
    work_domains = ['abacus.ai', 'lambdatest.com', 'github.com', 'slack.com', 'jira', 'confluence']
    work_keywords = ['meeting', 'project', 'task', 'build', 'test', 'deployment', 'review']
    
    if any(domain in sender_lower for domain in work_domains) or \
       any(keyword in subject_lower for keyword in work_keywords):
        return 'Work'
    
    # Personal email domains
    personal_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
    if any(domain in sender_lower for domain in personal_domains):
        return 'Personal'
    
    return 'Other'

def extract_domain(email):
    """Extract domain from email address"""
    if '@' in email:
        return email.split('@')[1]
    return email

def analyze_email_activity():
    """Analyze email activity and generate summary"""
    
    # Load data from all three searches
    received_data = load_email_data('/home/ubuntu/.external_service_outputs/gmail_tool_output_1752570411.json')
    sent_data = load_email_data('/home/ubuntu/.external_service_outputs/gmail_tool_output_1752570426.json')
    urgent_data = load_email_data('/home/ubuntu/.external_service_outputs/gmail_tool_output_1752570441.json')
    
    received_emails = received_data.get('results', [])
    sent_emails = sent_data.get('results', [])
    urgent_emails = urgent_data.get('results', [])
    
    # Basic counts
    total_received = len(received_emails)
    total_sent = len(sent_emails)
    total_urgent = len(urgent_emails)
    
    # Analyze received emails
    senders = []
    subjects = []
    email_types = Counter()
    sender_domains = Counter()
    
    for email in received_emails:
        sender = email.get('from', '')
        subject = email.get('subject', '')
        snippet = email.get('snippet', '')
        
        senders.append(sender)
        subjects.append(subject)
        
        # Categorize email type
        email_type = categorize_email_type(sender, subject, snippet)
        email_types[email_type] += 1
        
        # Track sender domains
        domain = extract_domain(sender)
        sender_domains[domain] += 1
    
    # Count unique senders
    unique_senders = Counter(senders)
    
    # Generate summary
    summary = f"""# Gmail Activity Summary - Past 24 Hours
*Generated on: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}*

## 📊 Overview
- **Total Emails Received:** {total_received}
- **Total Emails Sent:** {total_sent}
- **Urgent/Important Emails:** {total_urgent}
- **Overall Activity Level:** {'Low' if total_received + total_sent < 5 else 'Moderate' if total_received + total_sent < 20 else 'High'}

## 📧 Email Breakdown by Type
"""
    
    if email_types:
        for email_type, count in email_types.most_common():
            percentage = (count / total_received * 100) if total_received > 0 else 0
            summary += f"- **{email_type}:** {count} emails ({percentage:.1f}%)\n"
    else:
        summary += "- No emails to categorize\n"
    
    summary += "\n## 👥 Top Senders\n"
    if unique_senders:
        for sender, count in unique_senders.most_common(5):
            summary += f"- **{sender}:** {count} email{'s' if count > 1 else ''}\n"
    else:
        summary += "- No senders to display\n"
    
    summary += "\n## 🏢 Sender Domains\n"
    if sender_domains:
        for domain, count in sender_domains.most_common(5):
            summary += f"- **{domain}:** {count} email{'s' if count > 1 else ''}\n"
    else:
        summary += "- No domains to display\n"
    
    summary += "\n## 📋 Recent Email Subjects\n"
    if subjects:
        for subject in subjects[:10]:  # Show up to 10 most recent subjects
            summary += f"- {subject}\n"
    else:
        summary += "- No subjects to display\n"
    
    summary += "\n## ⚠️ Urgent/Priority Items\n"
    if total_urgent > 0:
        summary += f"- Found {total_urgent} urgent or important emails that may need attention\n"
        for email in urgent_emails[:5]:  # Show up to 5 urgent emails
            summary += f"  - **{email.get('subject', 'No Subject')}** from {email.get('from', 'Unknown')}\n"
    else:
        summary += "- No urgent or high-priority emails found\n"
    
    summary += "\n## 📈 Activity Patterns\n"
    if total_received > 0:
        # Analyze timing if we have date information
        summary += f"- Most recent activity shows {total_received} incoming message{'s' if total_received != 1 else ''}\n"
        if total_sent == 0:
            summary += "- No outgoing emails sent in the past 24 hours\n"
        else:
            summary += f"- {total_sent} outgoing email{'s' if total_sent != 1 else ''} sent\n"
    else:
        summary += "- Very quiet email day with minimal activity\n"
    
    summary += "\n## 💡 Key Insights & Recommendations\n"
    
    if total_received == 0 and total_sent == 0:
        summary += "- **Very Low Activity:** No email activity in the past 24 hours\n"
    elif total_received > 0 and total_sent == 0:
        summary += "- **Incoming Only:** You received emails but haven't sent any responses\n"
        summary += "- **Action Needed:** Consider reviewing received emails for any that require responses\n"
    
    if email_types.get('System/Automated', 0) > 0:
        summary += "- **Automated Emails:** You have system/automated emails that may contain important updates\n"
    
    if email_types.get('Work', 0) > 0:
        summary += "- **Work Activity:** Work-related emails detected - review for any urgent tasks or deadlines\n"
    
    if total_urgent == 0:
        summary += "- **No Urgent Items:** No emails marked as urgent or important\n"
    
    summary += "\n---\n*This summary was automatically generated based on your Gmail activity from the past 24 hours.*"
    
    return summary

if __name__ == "__main__":
    summary = analyze_email_activity()
    print(summary)
