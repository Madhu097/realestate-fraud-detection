# System Architecture Diagrams - Description Guide

## Overview

This document provides detailed descriptions for creating three key diagrams for your academic report. These can be easily recreated in Draw.io, PowerPoint, or any diagramming tool.

---

## DIAGRAM 1: System Architecture Diagram

### Purpose
Shows the overall system structure with all components and their interactions.

### Components to Draw

#### Layer 1: User Interface (Top)
```
┌─────────────────────────────────────────────┐
│         WEB BROWSER (User Interface)        │
│  ┌─────────────────────────────────────┐   │
│  │   React Frontend (Port 5173)        │   │
│  │   - Input Form                      │   │
│  │   - Results Dashboard               │   │
│  │   - History View                    │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    ↓ HTTP/REST API
```

#### Layer 2: Backend API (Middle)
```
┌─────────────────────────────────────────────┐
│      FastAPI Backend (Port 8000)            │
│  ┌─────────────────────────────────────┐   │
│  │   API Endpoints                     │   │
│  │   - /api/analyze                    │   │
│  │   - /api/history                    │   │
│  │   - /api/upload                     │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    ↓
```

#### Layer 3: Fraud Detection Modules (Core)
```
┌─────────────────────────────────────────────────────────┐
│           FRAUD DETECTION ENGINE                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │  Price   │  │  Image   │  │   Text   │  │Location ││
│  │  Fraud   │  │  Fraud   │  │  Fraud   │  │  Fraud  ││
│  │  Module  │  │  Module  │  │  Module  │  │  Module ││
│  │          │  │          │  │          │  │         ││
│  │ Z-score  │  │ Metadata │  │ Keyword  │  │ Coord   ││
│  │ Analysis │  │ Analysis │  │ Matching │  │ Verify  ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
│         ↓            ↓            ↓            ↓        │
│  ┌─────────────────────────────────────────────────┐   │
│  │         FUSION ENGINE                           │   │
│  │  Weighted Linear Combination                    │   │
│  │  Weights: 0.30, 0.25, 0.25, 0.20              │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                    ↓
```

#### Layer 4: Data Layer (Bottom)
```
┌─────────────────────────────────────────────┐
│         DATA STORAGE                        │
│  ┌──────────────┐    ┌──────────────┐      │
│  │   SQLite     │    │   CSV        │      │
│  │   Database   │    │   Dataset    │      │
│  │              │    │              │      │
│  │ - History    │    │ - 6,347      │      │
│  │ - Analysis   │    │   Properties │      │
│  │   Results    │    │              │      │
│  └──────────────┘    └──────────────┘      │
└─────────────────────────────────────────────┘
```

### Drawing Instructions

1. **Create 4 horizontal layers** (top to bottom)
2. **Use rectangles** for components
3. **Use arrows** to show data flow (downward)
4. **Color coding**:
   - Frontend: Light Blue (#E3F2FD)
   - Backend API: Light Green (#E8F5E9)
   - Fraud Modules: Light Orange (#FFF3E0)
   - Fusion Engine: Light Purple (#F3E5F5)
   - Data Layer: Light Gray (#F5F5F5)

### Labels to Include

**Frontend Box**:
- "React Frontend"
- "Vite + Tailwind CSS"
- "Port 5173"

**Backend Box**:
- "FastAPI Backend"
- "Python 3.9+"
- "Port 8000"

**Each Module Box**:
- Module name
- Detection method
- Output: "Fraud Score (0-1)"

**Fusion Engine Box**:
- "Weighted Linear Combination"
- "Final Fraud Probability"
- "Fraud Type Identification"

**Database Boxes**:
- "SQLite" → "Analysis History"
- "CSV" → "Training Dataset"

---

## DIAGRAM 2: Data Flow Diagram

### Purpose
Shows how data flows through the system from input to output.

### Flow Steps

```
START
  ↓
┌─────────────────────────────────────┐
│  1. USER INPUT                      │
│  - Title, Description               │
│  - Price, Area                      │
│  - City, Locality                   │
│  - Latitude, Longitude              │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  2. FRONTEND VALIDATION             │
│  - Required fields check            │
│  - Data type validation             │
│  - Range validation                 │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  3. API REQUEST                     │
│  POST /api/analyze                  │
│  Content-Type: application/json     │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  4. BACKEND VALIDATION              │
│  - Schema validation (Pydantic)     │
│  - Business rule validation         │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────┐
│  5. PARALLEL MODULE EXECUTION                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────┐│
│  │  Price   │  │  Image   │  │   Text   │  │ Loc ││
│  │  Module  │  │  Module  │  │  Module  │  │ Mod ││
│  └──────────┘  └──────────┘  └──────────┘  └─────┘│
│       ↓              ↓              ↓          ↓   │
│  Score: 0.85    Score: 0.0     Score: 0.75  0.65  │
└─────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  6. FUSION ENGINE                   │
│  Final = 0.30×P + 0.25×I +          │
│          0.25×T + 0.20×L            │
│  = 0.30×0.85 + 0.25×0 +             │
│    0.25×0.75 + 0.20×0.65            │
│  = 0.573                            │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  7. FRAUD TYPE IDENTIFICATION       │
│  IF module_score > 0.6:             │
│    Add to fraud_types[]             │
│  Result: ["Price Fraud"]            │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  8. EXPLANATION GENERATION          │
│  - Price: "80% below market avg"    │
│  - Text: "No suspicious patterns"   │
│  - Location: "Coordinates valid"    │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  9. DATABASE STORAGE                │
│  Save to history table:             │
│  - Listing data                     │
│  - Fraud probability                │
│  - Fraud types                      │
│  - Timestamp                        │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  10. API RESPONSE                   │
│  {                                  │
│    "fraud_probability": 0.573,      │
│    "fraud_types": ["Price Fraud"],  │
│    "module_scores": {...},          │
│    "explanations": [...]            │
│  }                                  │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  11. FRONTEND DISPLAY               │
│  - Fraud probability gauge          │
│  - Fraud type badges                │
│  - Module scores chart              │
│  - Explanation cards                │
└─────────────────────────────────────┘
  ↓
END
```

### Drawing Instructions

1. **Use vertical flowchart** (top to bottom)
2. **Rectangles** for processes
3. **Diamonds** for decisions (if any)
4. **Arrows** for flow direction
5. **Number each step** (1-11)
6. **Group related steps** with background colors

### Color Coding

- **Input/Output**: Light Blue
- **Validation**: Light Yellow
- **Processing**: Light Green
- **Storage**: Light Gray
- **Display**: Light Purple

---

## DIAGRAM 3: Fraud Detection Pipeline

### Purpose
Detailed view of how each fraud module works.

### Module-by-Module Breakdown

#### Price Fraud Module
```
INPUT: price, area_sqft, locality
  ↓
┌─────────────────────────────────────┐
│  1. Load Historical Data            │
│  Filter by locality                 │
│  Get price distribution             │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  2. Calculate Statistics            │
│  Mean = μ                           │
│  Std Dev = σ                        │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  3. Compute Z-Score                 │
│  z = (price - μ) / σ                │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  4. Map to Fraud Score              │
│  IF |z| > 2: score = 0.8-1.0        │
│  IF |z| > 1: score = 0.4-0.8        │
│  ELSE: score = 0.0-0.4              │
└─────────────────────────────────────┘
  ↓
OUTPUT: fraud_score, explanation
```

#### Text Fraud Module
```
INPUT: title, description
  ↓
┌─────────────────────────────────────┐
│  1. Text Preprocessing              │
│  - Convert to lowercase             │
│  - Remove special characters        │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  2. Keyword Matching                │
│  Check for:                         │
│  - Urgency: "URGENT", "HURRY"       │
│  - Scam: "GUARANTEED", "CASH ONLY"  │
│  - Exaggeration: "BEST", "PERFECT"  │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  3. Score Calculation               │
│  score = (matches / total) × weight │
└─────────────────────────────────────┘
  ↓
OUTPUT: fraud_score, matched_keywords
```

#### Location Fraud Module
```
INPUT: city, locality, latitude, longitude
  ↓
┌─────────────────────────────────────┐
│  1. Geocoding                       │
│  Get expected coordinates for       │
│  locality using geocoding API       │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  2. Distance Calculation            │
│  Haversine formula:                 │
│  d = distance(expected, provided)   │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  3. Fraud Score Mapping             │
│  IF d > 50km: score = 0.8-1.0       │
│  IF d > 10km: score = 0.4-0.8       │
│  ELSE: score = 0.0-0.4              │
└─────────────────────────────────────┘
  ↓
OUTPUT: fraud_score, distance_km
```

#### Image Fraud Module (Placeholder)
```
INPUT: image_file
  ↓
┌─────────────────────────────────────┐
│  PLACEHOLDER IMPLEMENTATION         │
│  Currently returns:                 │
│  - score = 0.0                      │
│  - explanation = "Not implemented"  │
└─────────────────────────────────────┘
  ↓
OUTPUT: fraud_score = 0.0
```

### Fusion Engine Detail
```
INPUT: All module scores
  ↓
┌─────────────────────────────────────┐
│  1. Weighted Combination            │
│  final = Σ(weight_i × score_i)      │
│                                     │
│  Weights:                           │
│  - Price: 0.30 (30%)                │
│  - Image: 0.25 (25%)                │
│  - Text: 0.25 (25%)                 │
│  - Location: 0.20 (20%)             │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  2. Fraud Type Identification       │
│  FOR each module:                   │
│    IF score > 0.6:                  │
│      Add to fraud_types[]           │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  3. Explanation Aggregation         │
│  Combine all module explanations    │
│  Sort by relevance                  │
└─────────────────────────────────────┘
  ↓
OUTPUT: FraudReport
  - fraud_probability
  - fraud_types[]
  - module_scores{}
  - explanations[]
```

### Drawing Instructions

1. **Create 4 separate sub-diagrams** (one per module + fusion)
2. **Use vertical flowcharts**
3. **Rectangles** for processes
4. **Rounded rectangles** for input/output
5. **Different colors** for each module
6. **Show formulas** in boxes

---

## Quick Reference: Component Labels

### For System Architecture Diagram

**Frontend Components**:
- React Frontend (Vite)
- Input Form Component
- Results Dashboard Component
- History View Component
- Axios HTTP Client

**Backend Components**:
- FastAPI Application
- API Router (/api/analyze)
- Pydantic Validators
- CORS Middleware

**Fraud Modules**:
- Price Fraud Detector (Z-score)
- Image Fraud Detector (Placeholder)
- Text Fraud Detector (Keywords)
- Location Fraud Detector (Haversine)

**Fusion Engine**:
- Weighted Linear Combiner
- Fraud Type Identifier
- Explanation Aggregator

**Data Layer**:
- SQLite Database (History)
- CSV Dataset (6,347 properties)
- Pandas DataFrames (In-memory)

---

## Drawing Tools Recommendations

### Draw.io (Free, Web-based)
- Use "Flowchart" shapes
- Use "UML" shapes for components
- Export as PNG (high resolution)

### Microsoft PowerPoint
- Use SmartArt for flowcharts
- Use shapes for architecture
- Group related components

### Lucidchart (Free tier available)
- Professional templates
- Collaboration features
- Export to multiple formats

---

## Tips for Academic Diagrams

1. **Keep it Simple**: Don't overcomplicate
2. **Use Consistent Colors**: Same component = same color
3. **Label Everything**: No unlabeled boxes
4. **Show Data Flow**: Use arrows with labels
5. **Add Legend**: Explain colors and symbols
6. **High Resolution**: Export at 300 DPI minimum
7. **Black & White Compatible**: Use patterns if needed

---

## Diagram Placement in Report

**System Architecture Diagram**:
- Chapter 4: Proposed System
- Chapter 5: System Architecture

**Data Flow Diagram**:
- Chapter 6: Methodology
- Section: System Workflow

**Fraud Detection Pipeline**:
- Chapter 6: Methodology
- Section: Fraud Detection Algorithms

---

**Diagram Guide Version**: 1.0  
**Last Updated**: January 20, 2026  
**Status**: ✅ Ready for Drawing  
**Total Diagrams**: 3
