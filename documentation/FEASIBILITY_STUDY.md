# Feasibility Study

## Technical feasibility
The project uses Python, Flask, SQLite, HTML, CSS and JavaScript. These technologies are widely available, have documentation and can run on a standard student laptop. Flask is suitable for a small modular web application and SQLite avoids the need for a separate database server.

## Economic feasibility
The software stack is open source and can be developed using free tools. The project does not require paid hosting or a payment gateway for local demonstration.

## Operational feasibility
The interface follows familiar ticket-booking workflows: browse, choose show, select seats, confirm, and view ticket. An administrator can manage the catalogue and show schedule through protected pages.

## Schedule feasibility
The work can be completed in stages: requirements, design, implementation, testing, documentation and GitHub publication. The provided prototype gives a runnable baseline that can be extended.

## Risks and mitigation
| Risk | Mitigation |
|---|---|
| Duplicate seat selection by concurrent users | Unique database constraint on show and seat |
| Password exposure | Store password hashes, not plain-text passwords |
| Accidental admin access | Role check on admin routes |
| Loss of local data | Back up the SQLite database |
| Demo payment mistaken for real payment | Label payment and ticket as demo-only |
