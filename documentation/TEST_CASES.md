# Test Cases

| ID | Test scenario | Steps / input | Expected result |
|---|---|---|---|
| TC-01 | Register valid user | Submit name, unique email and password >= 6 chars | Account is created |
| TC-02 | Duplicate registration | Register with an existing email | Error message shown |
| TC-03 | Login valid user | Enter correct email and password | User is logged in |
| TC-04 | Login invalid user | Enter incorrect password | Login rejected |
| TC-05 | Browse catalogue | Open home page | Movie/event cards are displayed |
| TC-06 | View show schedule | Open a listing | Future shows are displayed |
| TC-07 | Access seat map unauthenticated | Open a seat URL while logged out | Redirect to login |
| TC-08 | Book available seats | Select two available seats and confirm | Booking and ticket are created |
| TC-09 | Empty seat selection | Submit with no seats selected | Booking is rejected |
| TC-10 | Duplicate seat booking | Attempt to book a seat already booked for same show | Booking rejected; seat remains booked |
| TC-11 | Cancel booking | Cancel a confirmed booking | Status changes to CANCELLED and seats are released |
| TC-12 | Admin route as customer | Open /admin as a normal user | Access denied |
| TC-13 | Add listing as admin | Submit valid listing details | Listing appears in catalogue |
| TC-14 | Add show as admin | Submit date, time and prices | Show appears in listing schedule |
| TC-15 | Print ticket | Open ticket and use Print | Browser print dialog opens |

## Test execution record
Record actual results during testing. Do not mark a test as passed until it has been run.

| Test ID | Actual result | Status | Remarks |
|---|---|---|---|
| TC-01 to TC-15 | To be completed by project team | Not executed | Fill after running the application |
