# 🔍 Troubleshoot: No Email Received

## Quick Checks

### 1. Check if Lambda Function is Updated
The Lambda function needs to be deployed with the latest code:

```bash
# Check when function was last updated
aws lambda get-function --function-name RegisterFace --region us-east-1 --query 'Configuration.LastModified'
```

If it's older than today, you need to deploy the update.

### 2. Check SNS Subscriptions
```bash
aws sns list-subscriptions-by-topic \
    --topic-arn arn:aws:sns:us-east-1:846863292978:attendance-notifications \
    --region us-east-1
```

If empty, no emails have been subscribed yet.

### 3. Check Lambda Logs
```bash
aws logs tail /aws/lambda/RegisterFace --follow --region us-east-1
```

Look for:
- "Email subscription initiated"
- "Welcome email sent successfully"
- Any error messages

### 4. Check Spam Folder
AWS SNS emails often go to spam. Check:
- Spam/Junk folder
- Promotions tab (Gmail)
- All Mail folder

---

## 🚀 Deploy the Fix

The updated code needs to be deployed:

```bash
python deploy_lambda.py
```

This will:
1. Package the updated Lambda function
2. Deploy to AWS
3. Update the RegisterFace function

---

## 🧪 Test After Deployment

1. **Create a new account** with your email
2. **Check email immediately** (including spam)
3. **Look for AWS SNS confirmation email**
4. **Click confirmation link**
5. **Create another account** - should receive welcome email

---

## 📧 What to Expect

### First Email (Confirmation):
- **From:** no-reply@sns.amazonaws.com
- **Subject:** "AWS Notification - Subscription Confirmation"
- **Contains:** Confirmation link
- **Action:** Click the link to confirm

### Second Email (Welcome):
- **From:** AWS SNS (via your topic)
- **Subject:** "Welcome to Face Recognition Attendance System"
- **Contains:** Welcome message with account details

---

## ⚠️ Common Issues

### No Email at All:
1. **Lambda not deployed** - Deploy the updated function
2. **Email not in request** - Check frontend is sending email
3. **SNS topic issue** - Verify topic exists

### Confirmation Email but No Welcome:
1. **Subscription not confirmed** - Click the confirmation link
2. **Welcome sent before confirmation** - Create another account after confirming

### Emails Going to Spam:
1. **Check spam folder**
2. **Mark as not spam**
3. **Add AWS to contacts**

---

## 🔧 Manual Test

Test the SNS subscription manually:

```bash
# Subscribe your email
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:846863292978:attendance-notifications \
    --protocol email \
    --notification-endpoint "your-email@example.com" \
    --region us-east-1

# Check subscription status
aws sns list-subscriptions-by-topic \
    --topic-arn arn:aws:sns:us-east-1:846863292978:attendance-notifications \
    --region us-east-1
```

You should receive a confirmation email. After confirming, test sending:

```bash
aws sns publish \
    --topic-arn arn:aws:sns:us-east-1:846863292978:attendance-notifications \
    --subject "Test Email" \
    --message "This is a test message" \
    --region us-east-1
```

---

## ✅ Next Steps

1. **Deploy the updated Lambda function**
2. **Test with a new account**
3. **Check spam folder for confirmation email**
4. **Confirm subscription**
5. **Test again**

The fix is in the code - it just needs to be deployed!

