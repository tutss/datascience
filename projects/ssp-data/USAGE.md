# Crime analysis usage guide

## Basic usage (citywide only)

```bash
conda activate ai
cd projects/ssp-data
python generate_insights.py --year 2024
```

This generates 11 citywide visualizations in `output/` directory.

## Neighborhood-specific analysis

For your Zona Sul neighborhoods:

```bash
python generate_insights.py --year 2024 --neighborhoods \
  conceicao conceição jabaquara \
  "vila guarani(zona sul)" "vila guarani" \
  "vila guarani (z sul)" "vila guarani (zona sul)" \
  "vila monte alegre"
```

This generates:
- **11 citywide visualizations** (same as basic usage)
- **7 neighborhood-specific visualizations**:
  - `neighborhood_comparison.png` - Your neighborhoods vs top 10 SP neighborhoods
  - `neighborhood_crime_breakdown.png` - Crime types in your neighborhoods
  - `neighborhood_time_series.png` - Daily trend with 7-day moving average
  - `neighborhood_hourly_pattern.png` - When crimes occur (day × hour heatmap)
  - `neighborhood_monthly_change.png` - Month-by-month evolution (Jan-Jun)
  - `neighborhood_vs_citywide.png` - Your crime profile vs São Paulo overall
  - `neighborhood_safety_breakdown.csv` - Individual stats for each neighborhood

## Examples

### Analyze only 2023 data
```bash
python generate_insights.py --input SPDadosCriminais_2023.xlsx --year 2023
```

### Custom output directory
```bash
python generate_insights.py --year 2024 --output-dir analysis_2024
```

### Different neighborhoods
```bash
python generate_insights.py --year 2024 --neighborhoods pinheiros "jardim paulista" itaim
```

## What the neighborhood analysis tells you

1. **neighborhood_comparison.png**: Are you in a high-crime or low-crime area?
2. **neighborhood_crime_breakdown.png**: What specific crimes affect YOUR area?
3. **neighborhood_time_series.png**: Is crime increasing or decreasing in your neighborhoods?
4. **neighborhood_hourly_pattern.png**: When should you be most cautious?
5. **neighborhood_monthly_change.png**: How has the situation evolved over 2024?
6. **neighborhood_vs_citywide.png**: Does your area have different crime patterns than SP overall?
7. **neighborhood_safety_breakdown.csv**: Which specific neighborhood is safest/riskiest?
