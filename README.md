# Deep Research clone

```bash
uv run main.py
```

## Flow

1. Enters your research topic

2. Then the `planner_agent` comes up with a plan to search the web for information. The plan is a list of search queries, with a search term and a reason for each query.

3. `critique_agent` then critiques the plan and provides improvements to ensure the users request is well served.

4. For each search item, we run a `search_agent`, which uses the Web Search tool to search for that term and summarise the results. These all run in parallel.

5. Finally, the `writer_agent` receives the search summaries, and creates a written report output in the terminal.

Cool terminal outputs are created with `rich`.