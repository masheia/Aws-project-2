# 📍 Setup School Coordinates for Geofencing

## ⚠️ IMPORTANT: Update School Location

You **MUST** update the school coordinates in the Lambda functions before deploying!

---

## Step 1: Get Your School's Coordinates

### Method 1: Google Maps (Easiest)

1. Go to https://www.google.com/maps
2. Search for your school name
3. Right-click on the school location
4. Click the coordinates that appear (e.g., "40.7128, -74.0060")
5. Copy the coordinates

### Method 2: Use Your Phone

1. Open Google Maps on your phone
2. Navigate to your school
3. Long-press on the school location
4. Coordinates will appear at the bottom
5. Copy them

### Method 3: Online Tools

- Use https://www.latlong.net/
- Enter your school address
- Get coordinates

---

## Step 2: Update Lambda Functions

You need to update **TWO** Lambda function files:

### File 1: `lambda-functions/manage-faces/lambda_function.py`

Find these lines (around line 25-27):
```python
SCHOOL_LATITUDE = 40.7128   # TODO: Update with your school's latitude
SCHOOL_LONGITUDE = -74.0060  # TODO: Update with your school's longitude
ALLOWED_RADIUS_METERS = 500  # Allowed radius in meters
```

**Replace with your school's coordinates:**
```python
SCHOOL_LATITUDE = YOUR_SCHOOL_LATITUDE   # e.g., 40.7589
SCHOOL_LONGITUDE = YOUR_SCHOOL_LONGITUDE  # e.g., -73.9851
ALLOWED_RADIUS_METERS = 500  # Adjust radius as needed (500m = ~0.3 miles)
```

### File 2: `lambda-functions/process-attendance/lambda_function.py`

Find the same lines and update them with the **same coordinates**.

---

## Step 3: Configure Radius

**ALLOWED_RADIUS_METERS** determines how far from school center is allowed:

- **100 meters** (~0.06 miles) - Very strict, only school building
- **500 meters** (~0.3 miles) - Default, covers school campus
- **1000 meters** (~0.6 miles) - Covers larger campus area
- **2000 meters** (~1.2 miles) - Very permissive

**Recommendation:** Start with 500 meters and adjust as needed.

---

## Step 4: Deploy Updated Functions

After updating coordinates:

```bash
python deploy_lambda.py
```

This will deploy both Lambda functions with your school coordinates.

---

## Step 5: Test

1. **Test from school location:**
   - Should work ✅

2. **Test from outside school:**
   - Should be rejected ❌
   - Error message will show distance from school

---

## Example Configuration

For a school in New York:
```python
SCHOOL_LATITUDE = 40.7589    # Your school's latitude
SCHOOL_LONGITUDE = -73.9851  # Your school's longitude
ALLOWED_RADIUS_METERS = 500  # 500 meters from school center
```

---

## 🔒 Security Settings

### Strict Mode (Recommended)
```python
REQUIRE_LOCATION = True  # Reject uploads without location
```
- Most secure
- Requires location permission
- Rejects if location denied

### Flexible Mode
```python
REQUIRE_LOCATION = False  # Allow uploads if location unavailable
```
- Better user experience
- Still validates when location provided
- Less secure (allows uploads if location denied)

---

## 📝 Quick Reference

**Files to Update:**
1. `lambda-functions/manage-faces/lambda_function.py` (lines ~25-27)
2. `lambda-functions/process-attendance/lambda_function.py` (lines ~25-27)

**What to Update:**
- `SCHOOL_LATITUDE` - Your school's latitude
- `SCHOOL_LONGITUDE` - Your school's longitude
- `ALLOWED_RADIUS_METERS` - Distance allowed (default: 500)

**After Updating:**
- Run `python deploy_lambda.py` to deploy

---

## ⚠️ Important Notes

- **Coordinates must be in decimal degrees** (e.g., 40.7128, not 40°42'46")
- **Latitude range:** -90 to 90
- **Longitude range:** -180 to 180
- **Both functions must have the same coordinates**
- **Test after deployment** to ensure it works

---

## 🧪 Verification

After deployment, test:

1. **From school:** Should work ✅
2. **From home (outside):** Should be rejected ❌
3. **Error message:** Should show distance from school

The system is ready once you update the coordinates!

