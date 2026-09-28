# Research Intelligence

A modular seven-agent research system built with CrewAI, Groq and Streamlit.

## Overview

Research Intelligence decomposes a research question into specialized investigations.

The system uses seven agents:

1. Research Planner
2. Web Researcher
3. Academic Researcher
4. Industry Researcher
5. Evidence Analyst
6. Fact Checker
7. Research Synthesizer

## Architecture

User -> Research Planner -> Web Researcher + Academic Researcher + Industry Researcher -> Evidence Analyst -> Fact Checker -> Research Synthesizer -> Final Research Report

## Tools

### Web Research

Tavily Search and Tavily Extract.

### Academic Research

OpenAlex Works API.




