-- Enable UUID extension for unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. DEALS LEDGER (The Raw Capital)
-- Stores every incoming pitch from Tally
CREATE TABLE deals_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    -- Founder Data (from Tally)
    startup_name TEXT,
    founder_name TEXT,
    founder_email TEXT,
    pitch_text TEXT,
    deck_url TEXT,
    
    -- Analysis Data (from AI)
    sector TEXT,
    tech_stack_rating INT, -- 0-10 Score
    market_score INT,      -- 0-10 Score
    analysis_report TEXT,  -- Full AI Feedback
    
    -- Status
    status TEXT DEFAULT 'PENDING', -- PENDING, PROCESSED, REJECTED, MEETING
    
    -- Metadata
    tally_response_id TEXT
);

-- 2. FOUNDER INDEX (The KYC)
-- Enriched profiles of founders (LinkedIn data, past exits)
CREATE TABLE founder_index (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    founder_email TEXT UNIQUE,
    linkedin_url TEXT,
    
    -- Enrichment Data
    is_technical BOOLEAN DEFAULT FALSE,
    years_experience INT,
    past_exits INT DEFAULT 0,
    github_url TEXT
);

-- 3. MARKET BENCHMARKS (The Exchange Rate)
-- Your "100 Startups" database for comparisons
CREATE TABLE market_benchmarks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    startup_name TEXT,
    sector TEXT,
    outcome TEXT, -- 'UNICORN', 'ACQUIRED', 'FAILED', 'ZOMBIE'
    
    -- The "Why"
    winning_factor TEXT, -- e.g. "PLG Motion"
    failure_reason TEXT  -- e.g. "High CAC"
);

-- 4. OUTBOX (The Wire Transfers)
-- Queue for emails to be sent by the Worker
CREATE TABLE outbox (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    recipient_email TEXT,
    subject TEXT,
    body_text TEXT,
    
    status TEXT DEFAULT 'QUEUED', -- QUEUED, SENT, FAILED
    sent_at TIMESTAMP WITH TIME ZONE
);

-- 5. PORTFOLIO LEDGER (The Vault)
-- Your actual (or phantom) investments
CREATE TABLE portfolio_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    startup_name TEXT,
    investment_date DATE,
    amount_invested NUMERIC,
    valuation_cap NUMERIC,
    
    current_status TEXT -- 'ACTIVE', 'DEAD', 'EXIT'
);

-- 6. PORTFOLIO METRICS (Automated Board Member)
-- Monthly updates from portfolio companies
CREATE TABLE portfolio_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    startup_id UUID REFERENCES portfolio_ledger(id),
    month DATE,
    
    mrr NUMERIC,
    burn_rate NUMERIC,
    runway_months NUMERIC,
    headcount INT
);

-- 7. REGULATORY RADAR (The Watchtower)
-- Keywords to track for risk management
CREATE TABLE regulatory_watch (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    keyword TEXT, -- e.g. "RBI", "GST API"
    related_sector TEXT, -- e.g. "FinTech"
    last_checked_at TIMESTAMP WITH TIME ZONE
);
