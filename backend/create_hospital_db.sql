-- Create Clean Hospital Database
-- Run this in pgAdmin or psql

-- Step 1: Drop database if exists (optional - be careful!)
-- DROP DATABASE IF EXISTS hospital;

-- Step 2: Create database
CREATE DATABASE hospital;

-- Step 3: Connect to hospital database
-- \c hospital

-- Step 4: Verify connection
-- SELECT current_database();

-- Note: Tables will be created automatically when you run:
-- python init_clean_database.py
-- This will create EMPTY tables with no sample data
