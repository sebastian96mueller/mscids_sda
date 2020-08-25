# Sport Data Analytics

---

## Table of content
- [Task_1](#task-1)
- [Folder structure](#folder-structure)
- [Implementation details](#implementation-details)

### Task 1
The task consists of computing the real skill and luck ration of different competitors.

### Folder Structure
```tree
.
+-- src
|   +-- main.py
|   +-- request_team_statistics.py
+-- test
|   +-- test_request_team_statistics.py
+-- .gitignore
+-- README.md
```

### Implementation details
The class RequestTeamStatistics in request_team_statistics.py establishes a connection with the api. If successful, the team statistics are returned in the response.  
The response is parsed to access and calculate the total number of games played and number of games won (matches_played and matches_won).  


