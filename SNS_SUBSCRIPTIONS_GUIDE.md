# 📧 SNS Subscriptions Guide

## 🔍 Where to Find Subscriptions

### In AWS Console:

**Direct Link to Subscriptions:**
https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/subscriptions

**Or via Topic:**
1. Go to SNS Console → Topics
2. Click on `attendance-notifications` topic
3. Click the **"Subscriptions"** tab (you're already there!)

---

## 📊 Current Status

**Your Topic:** `attendance-notifications`  
**Subscriptions:** 0 (as shown in console)

---

## 🤔 Why Are There No Subscriptions?

Subscriptions are created automatically when:
1. **Student signs up** with email
2. **Lambda function subscribes** the email to the topic
3. **AWS sends confirmation email** to the student
4. **Student clicks confirmation link**
5. **Subscription becomes "Confirmed"**

### Possible Reasons for 0 Subscriptions:

1. **No students have signed up yet** with email addresses
2. **Students haven't confirmed** their email subscriptions yet
3. **Subscriptions are pending** (waiting for confirmation)
4. **Lambda function hasn't been called** with email addresses

---

## 🔍 Check All Subscriptions (Including Pending)

### Method 1: AWS Console

1. **Go to SNS Console:**
   https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/subscriptions

2. **View All Subscriptions:**
   - Shows all subscriptions across all topics
   - Look for subscriptions with Protocol: "email"
   - Check Status: "PendingConfirmation" or "Confirmed"

### Method 2: AWS CLI

```bash
# List all subscriptions (all topics)
aws sns list-subscriptions --region us-east-1

# List subscriptions for your topic only
aws sns list-subscriptions-by-topic \
    --topic-arn arn:aws:sns:us-east-1:846863292978:attendance-notifications \
    --region us-east-1
```

---

## 📧 Subscription Statuses

### PendingConfirmation
- **What it means:** Subscription created, waiting for email confirmation
- **Action needed:** Student must click confirmation link in email
- **Where:** Check student's email inbox (and spam folder)

### Confirmed
- **What it means:** Subscription is active
- **Action needed:** None - ready to receive notifications
- **Status:** ✅ Working

### Deleted
- **What it means:** Subscription was removed
- **Action needed:** Re-subscribe if needed

---

## 🧪 Test: Create a Subscription Manually

To test if subscriptions work:

### Via Console:
1. Go to SNS Topic: `attendance-notifications`
2. Click **"Create subscription"** button
3. Choose **Protocol:** Email
4. Enter **Endpoint:** Your email address
5. Click **"Create subscription"**
6. Check your email for confirmation
7. Click confirmation link
8. Subscription becomes "Confirmed"

### Via CLI:
```bash
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:846863292978:attendance-notifications \
    --protocol email \
    --notification-endpoint "your-email@example.com" \
    --region us-east-1
```

---

## 🔍 Check if Students Have Emails in DynamoDB

Subscriptions are created when students sign up. Check if students have emails:

### Via Console:
1. Go to DynamoDB → `Students` table
2. View table items
3. Check if students have `Email` field

### Via CLI:
```bash
aws dynamodb scan \
    --table-name Students \
    --region us-east-1 \
    --query "Items[?Email].{StudentId:StudentId.S,Name:Name.S,Email:Email.S}" \
    --output table
```

---

## 📝 How Subscriptions Are Created

### Automatic Process:

1. **Student signs up** with email on website
2. **Frontend sends** email to Lambda function
3. **Lambda function** (`RegisterFace`) calls:
   ```python
   sns_client.subscribe(
       TopicArn=SNS_TOPIC_ARN,
       Protocol='email',
       Endpoint=email
   )
   ```
4. **AWS SNS** sends confirmation email to student
5. **Student clicks** confirmation link
6. **Subscription status** changes to "Confirmed"
7. **Future notifications** are delivered

---

## 🔍 Troubleshooting

### If No Subscriptions Appear:

1. **Check if students have emails:**
   - Go to DynamoDB → Students table
   - Verify students have `Email` field

2. **Check Lambda logs:**
   ```bash
   aws logs tail /aws/lambda/RegisterFace --follow --region us-east-1
   ```
   - Look for "Email subscription initiated"
   - Look for any errors

3. **Check all subscriptions** (not just topic):
   - Go to: https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/subscriptions
   - May show pending subscriptions

4. **Test manually:**
   - Create a test subscription
   - Verify you receive confirmation email

### If Subscriptions Are Pending:

- **Check student's email** (including spam)
- **Confirmation email** comes from: `no-reply@sns.amazonaws.com`
- **Subject:** "AWS Notification - Subscription Confirmation"
- **Action:** Student must click the link

---

## ✅ Expected Behavior

### When Student Signs Up:
1. Subscription created automatically
2. Status: "PendingConfirmation"
3. AWS sends confirmation email
4. After confirmation: Status becomes "Confirmed"
5. Student receives welcome email
6. Future attendance notifications work

---

## 📍 Where to Find Subscriptions

### Option 1: Via Topic (Current Location)
- You're already there!
- SNS Console → Topics → `attendance-notifications` → Subscriptions tab
- Shows subscriptions for this topic only

### Option 2: All Subscriptions
- SNS Console → Subscriptions (left sidebar)
- Shows all subscriptions across all topics
- https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/subscriptions

### Option 3: AWS CLI
```bash
# All subscriptions
aws sns list-subscriptions --region us-east-1

# Topic-specific
aws sns list-subscriptions-by-topic \
    --topic-arn arn:aws:sns:us-east-1:846863292978:attendance-notifications \
    --region us-east-1
```

---

## 🎯 Quick Actions

### View All Subscriptions:
https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/subscriptions

### View Topic Subscriptions:
https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/topic/arn:aws:sns:us-east-1:846863292978:attendance-notifications

### Create Test Subscription:
1. Click "Create subscription" button
2. Protocol: Email
3. Endpoint: Your email
4. Create and confirm

---

## 💡 Summary

**Current Status:** 0 subscriptions (normal if no students have signed up yet or haven't confirmed)

**To See Subscriptions:**
- Check "Subscriptions" tab in the topic (where you are now)
- Or go to SNS → Subscriptions (left sidebar) to see all

**Subscriptions are created automatically** when students sign up with email addresses!

