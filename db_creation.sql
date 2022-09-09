-- Create the database
CREATE DATABASE IF NOT EXISTS project;

-- Use the database
USE project;

-- Create the tetor table
CREATE TABLE IF NOT EXISTS tetor (
    title VARCHAR(255) PRIMARY KEY, -- File names, unique
    summary TEXT                    -- File content
);
