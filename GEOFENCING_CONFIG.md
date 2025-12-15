# 📍 Geofencing Configuration

## School Area Boundaries

You need to define your school's geographic boundaries. Update these coordinates in the Lambda functions.

### How to Get School Coordinates

1. **Google Maps Method:**
   - Go to Google Maps
   - Find your school location
   - Right-click on the school
   - Click the coordinates to copy them
   - Format: Latitude, Longitude (e.g., 40.7128, -74.0060)

2. **Define School Boundaries:**
   - **School Center (Latitude, Longitude):** Your school's main location
   - **Radius (meters):** How far from center is allowed (e.g., 500m = ~0.3 miles)

### Example Configuration

```python
# School location (update these!)
SCHOOL_LATITUDE = 40.7128   # Your school's latitude
SCHOOL_LONGITUDE = -74.0060  # Your school's longitude
ALLOWED_RADIUS_METERS = 500  # 500 meters (~0.3 miles) from school center
```

---

## How It Works

1. **Frontend:** Requests user's location via browser geolocation API
2. **User grants permission:** Browser provides coordinates
3. **Coordinates sent:** Included with image upload request
4. **Lambda validates:** Checks if coordinates are within school area
5. **Accept/Reject:** Allows upload if within boundaries, rejects if outside

---

## Privacy & Security

- ✅ **User permission required** - Browser asks for location permission
- ✅ **Coordinates only** - No exact address stored
- ✅ **Optional fallback** - Can allow uploads if geolocation fails (configurable)
- ✅ **Server-side validation** - Can't be bypassed by client manipulation

---

## Configuration Options

### Strict Mode (Recommended)
- Reject all uploads without valid location
- Reject uploads outside school area
- Most secure

### Flexible Mode
- Allow uploads if geolocation fails (user denies permission)
- Still validate when coordinates are provided
- Better user experience, less strict security

---

## Update Instructions

1. **Get your school coordinates** (see above)
2. **Update Lambda functions** with your coordinates
3. **Deploy updated functions**
4. **Test with location enabled**

