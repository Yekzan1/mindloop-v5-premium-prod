-- ============================================================
-- MindLoop V6 — Supabase Database Schema
-- Run this in your Supabase SQL Editor (once)
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── USERS TABLE ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT,               -- NULL for OAuth users
    full_name     TEXT,
    avatar_url    TEXT,
    bio           TEXT,
    skills        TEXT[] DEFAULT '{}',
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    last_login    TIMESTAMPTZ DEFAULT NOW()
);

-- ── POSTS TABLE ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS posts (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
    content       TEXT NOT NULL,
    ai_summary    TEXT,
    ai_quiz       JSONB DEFAULT '[]',
    ai_tags       TEXT[] DEFAULT '{}',
    likes         INT DEFAULT 0,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ── ROW LEVEL SECURITY ────────────────────────────────────────
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if re-running
DROP POLICY IF EXISTS "users_select_all"   ON users;
DROP POLICY IF EXISTS "users_insert_all"   ON users;
DROP POLICY IF EXISTS "users_update_own"   ON users;
DROP POLICY IF EXISTS "posts_select_all"   ON posts;
DROP POLICY IF EXISTS "posts_insert_auth"  ON posts;

-- USERS: Anyone can read profiles
CREATE POLICY "users_select_all"
    ON users FOR SELECT USING (true);

-- USERS: Anyone can create an account (open signup)
CREATE POLICY "users_insert_all"
    ON users FOR INSERT WITH CHECK (true);

-- USERS: Only the owner can update their profile
CREATE POLICY "users_update_own"
    ON users FOR UPDATE USING (auth.uid()::text = id::text);

-- POSTS: Anyone can read posts
CREATE POLICY "posts_select_all"
    ON posts FOR SELECT USING (true);

-- POSTS: Authenticated users can insert posts
CREATE POLICY "posts_insert_auth"
    ON posts FOR INSERT WITH CHECK (true);
