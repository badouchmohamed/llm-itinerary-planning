# LLM-Guided Itinerary Planning Dataset and Code

This repository contains the datasets and code supporting the research article *"Personalized Itinerary Planning with LLM-Guided Interaction"* by Mohamed Badouch and Mehdi Boutaounte, submitted to *Electronics* (MDPI). The study evaluates a large language model (LLM)-guided system for personalized travel itinerary planning, comparing conversational, form-based, and hybrid interfaces using usability (System Usability Scale, SUS), cognitive load (NASA-TLX), efficiency, and satisfaction metrics.

## Repository Contents
- **Datasets**:
  - `travel_activities_50000.csv`: A dataset of 50,000 travel activities across 10 destinations, used for itinerary recommendations.
  - `user_study_logs.csv`: Interaction logs from a user study with 50 participants evaluating three interfaces (150 rows total).
- **Supplementary Materials**:
  - Additional figures and tables (e.g., raw SUS and NASA-TLX data) are referenced in the manuscript and available via Zenodo.

## Dataset Description

### 1. Travel Database (`travel_activities_50000.csv`)
- **Description**: A comprehensive dataset of 50,000 travel activities across 10 global destinations, curated for use in an LLM-based itinerary planning system.
- **Attributes**:
  - `ActivityID`: Unique identifier (1 to 50,000).
  - `Name`: Activity name (e.g., "Louvre Museum_1").
  - `Location`: One of 10 destinations (Paris, Tokyo, New York, London, Rome, Sydney, Barcelona, Bangkok, Cape Town, Rio de Janeiro).
  - `Type`: Activity type (Cultural, Outdoor, Family-friendly, Scenic, Historical).
  - `Cost`: Cost in USD (0 to 200).
  - `Duration`: Duration in hours (1 to 8).
  - `Rating`: User rating (3.0 to 5.0 stars).
- **Size**: 50,000 rows, approximately 10 MB.
- **Example**: ActivityID,Name,Location,Type,Cost,Duration,Rating 1,Louvre Museum_1,Paris,Cultural,142,4,4.5 2,Tokyo Skytree_2,Tokyo,Scenic,67,2,4.3 3,Central Park_3,New York,Outdoor,0,3,4.8


### 2. User Study Data (`user_study_logs.csv`)
- **Description**: Interaction logs from a user study with 50 participants planning 3-day trips using three interfaces (conversational, form-based, hybrid).
- **Attributes**:
- `ParticipantID`: Participant identifier (1 to 50).
- `Interface`: Interface type (Conversational, Form-based, Hybrid).
- `InputType`: Input method (Text, Slider, Text+Dropdown).
- `Input`: User input (e.g., "Make it family-friendly").
- `DwellTime`: Time spent viewing an activity (seconds).
- `Clicks`: Number of clicks per session (0 to 5).
- `SUS`: System Usability Scale score (0 to 100).
- `NASA_TLX`: Cognitive load score (0 to 100).
- `TimeToFinalize`: Time to complete itinerary (minutes).
- `Iterations`: Number of recommendation refinements.
- `Satisfaction`: User satisfaction (1 to 5 Likert scale).
- **Size**: 150 rows (50 participants × 3 interfaces), approximately 20 KB.
- **Example**: ParticipantID,Interface,InputType,Input,DwellTime,Clicks,SUS,NASA_TLX,TimeToFinalize,Iterations,Satisfaction 1,Conversational,Text,Make it family-friendly,14.2,3,78.5,40.1,15.3,4.4,4 1,Form-based,Slider,Budget ≤ $500,9.0,2,80.2,35.4,13.7,3.8,4 1,Hybrid,Text+Dropdown,Add outdoor activities; Duration ≤ 2h,12.8,4,87.0,29.3,11.9,3.1,5



### Contact
For questions, contact Mohamed Badouch at mohamed.badouch@edu.uiz.ac.ma.
