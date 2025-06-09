# Fiesta Data Releases Repository

This repository manages reference data releases for the **FiestaWare Collection** mobile app. It enables remote updates of Fiesta shapes, colors, and availability data without requiring app store updates.

## 🎯 Purpose

The FiestaWare Collection app can automatically download updated Fiesta reference data from GitHub releases, allowing:
- **New shape additions** (new Fiesta products)
- **New color releases** (seasonal colors, limited editions)
- **Availability updates** (shape-color combinations)
- **Data corrections** (hex codes, categorization, retirement dates)
- **Historical updates** (discontinued items, date corrections)

## 📱 How It Works

1. **App checks for updates** via GitHub API
2. **Compares versions** against currently installed data
3. **Downloads JSON file** from latest release assets
4. **Creates automatic backup** before updating
5. **Updates reference data** while preserving user inventory
6. **Records version history** for audit trail

## 🏷️ Version Numbering

Use **date-based semantic versioning**:

```
v2025.06.09    (June 9, 2025)
v2025.12.15    (December 15, 2025)
v2026.03.20    (March 20, 2026)
```

### Version Format Rules
- **Prefix**: Always start with `v`
- **Year**: Full 4-digit year (2025, 2026, etc.)
- **Month**: Zero-padded month (01-12)
- **Day**: Zero-padded day (01-31)
- **Separators**: Use dots (.) between components

### Comparison Logic
The app converts versions to integers for comparison:
- `v2025.06.09` → `20250609`
- `v2025.12.15` → `20251215`
- Higher numbers = newer versions

## 📁 Required File Format

Each release must include: **`fiesta_merged_with_categories.json`**

### JSON Structure
```json
[
  {
    "shape": "Dinner Plate",
    "color": "Scarlet",
    "hex": "#CC0000",
    "category": "Dinnerware",
    "introducedAt": 1986,
    "retiredAt": null,
    "isPost86": true
  },
  {
    "shape": "Mug",
    "color": "Shamrock",
    "hex": "#228B22",
    "category": "Drinkware", 
    "introducedAt": 1986,
    "retiredAt": 2025,
    "isPost86": true
  }
]
```

### Required Fields
- **`shape`** (string): Fiesta shape name (e.g., "Dinner Plate", "Medium Bowl")
- **`color`** (string): Fiesta color name (e.g., "Scarlet", "Shamrock")
- **`hex`** (string): Color hex code in #RRGGBB format (e.g., "#CC0000")
- **`category`** (string): Shape category for organization
- **`isPost86`** (boolean): Whether available in Post-1986 Fiesta line

### Optional Fields
- **`introducedAt`** (number|null): Year when color was introduced
- **`retiredAt`** (number|null): Year when color was retired (null if active)

### Categories
Use these standardized categories:
- **Dinnerware**: Plates, platters, serving pieces
- **Drinkware**: Mugs, cups, saucers, tumblers
- **Bowls**: All bowl types and sizes
- **Bakeware**: Baking dishes, pie plates, bakers
- **Serveware**: Serving bowls, trays, accessories
- **Countertop Accessories**: Kitchen tools, containers
- **Pitchers, Teapots & Vases**: Pouring vessels and vases
- **Shapes**: Novelty items (hearts, pumpkins, etc.)
- **Other**: Miscellaneous items

## 🚀 Creating a Release

### Step 1: Prepare Data File
1. **Generate/update** your `fiesta_merged_with_categories.json`
2. **Validate JSON syntax** (use online validator or `jq` tool)
3. **Verify required fields** are present for all records
4. **Check hex codes** are valid #RRGGBB format
5. **Test file size** (should be reasonable for mobile download)

### Step 2: Create GitHub Release
1. **Go to Releases** tab in this repository
2. **Click "Create a new release"**
3. **Set tag version**: Use format `v2025.06.09`
4. **Release title**: Descriptive name (e.g., "June 2025 Data Update")
5. **Description**: Write release notes explaining changes

### Step 3: Attach Data File
1. **Drag and drop** `fiesta_merged_with_categories.json` to release assets
2. **Verify file name** is exactly `fiesta_merged_with_categories.json`
3. **Check file size** appears reasonable
4. **Publish release**

### Example Release Notes
```markdown
## June 2025 Fiesta Data Update

### New Colors Added
- **Sage**: New 2025 color (#9CAF88)
- **Coral**: Limited edition summer color (#FF7F50)

### New Shapes
- 12-inch Oval Serving Platter
- Espresso Cup and Saucer Set

### Updates
- Fixed Mulberry hex code from #8B008B to #8E4585
- Updated Tangerine retirement date to 2024
- Recategorized Large Serving Bowl from "Other" to "Serveware"

### Data Statistics
- 52,847 total records
- 43 color variations
- 127 shape variations
- 15 categories
```

## 🔍 Validation & Testing

### Before Release
- [ ] JSON file validates successfully
- [ ] All required fields present
- [ ] Hex codes in #RRGGBB format
- [ ] Categories use standard names
- [ ] File size under 10MB
- [ ] Version number follows format

### After Release
- [ ] Release shows in GitHub API (`/repos/jtmurphysr/fiesta-data-releases/releases/latest`)
- [ ] JSON file accessible via download URL
- [ ] App detects update when checking for updates
- [ ] Update process completes successfully
- [ ] User data preserved after update

## 🛡️ Data Safety

The app's update system is designed for **100% user data safety**:

### What Gets Updated
- ✅ **Shapes table**: New shapes, updated categories
- ✅ **Colors table**: New colors, updated hex codes
- ✅ **Availability table**: Shape-color combinations

### What Stays Protected
- ✅ **User inventory**: All user items preserved
- ✅ **Wishlist items**: All wishlist entries preserved  
- ✅ **UUIDs**: Existing database IDs maintained
- ✅ **User settings**: All preferences retained

### Safety Mechanisms
- **Automatic backup** created before every update
- **UUID preservation** prevents broken references
- **Transaction rollback** if update fails
- **Validation checks** before applying changes

## 📊 Monitoring Updates

### GitHub API Access
The app uses these endpoints:
- **Latest release**: `GET /repos/jtmurphysr/fiesta-data-releases/releases/latest`
- **All releases**: `GET /repos/jtmurphysr/fiesta-data-releases/releases`
- **Asset download**: Asset `browser_download_url` from release data

### User Analytics
Track update adoption through:
- App analytics showing data version distribution
- User feedback on new shapes/colors
- Error reports from update failures

## 🔧 Troubleshooting

### Common Issues

#### Release Not Detected
- **Cause**: Version number format incorrect
- **Fix**: Use exact format `v2025.06.09`

#### Download Fails  
- **Cause**: File name incorrect or missing
- **Fix**: Ensure file named `fiesta_merged_with_categories.json`

#### JSON Parse Error
- **Cause**: Invalid JSON syntax
- **Fix**: Validate JSON before release

#### Update Fails
- **Cause**: Required fields missing or invalid
- **Fix**: Check all records have shape, color, hex, category

### Emergency Rollback
If an update causes issues:
1. **Users can restore** from automatic backup via app
2. **Delete problematic release** from GitHub
3. **Create corrected release** with incremented version

## 📞 Support

For technical issues with the release system:
- **App Issues**: Contact app development team
- **Data Issues**: Review this README and validate JSON
- **GitHub Issues**: Check repository settings and permissions

---

**Repository**: https://github.com/jtmurphysr/fiesta-data-releases  
**App**: FiestaWare Collection Mobile App  
**Last Updated**: June 2025 
