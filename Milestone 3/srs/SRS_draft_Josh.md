Functional Requirements 

FR-1. The system shall allow the user to select a BasicML program file from their computer. 

FR-2. The system shall load a valid BasicML program into memory. 

FR-3. The system shall display an error message when the selected program file is invalid or malformed. 

FR-4. The system shall allow the user to select another program file after a file-loading error without restarting the application. 

FR-5. The system shall allow the user to start execution of a successfully loaded BasicML program. 

FR-6. The system shall allow the user to stop a program while it is executing. 

FR-7. The system shall execute all 12 supported BasicML operations. 

FR-8. The system shall request input from the user when a READ instruction is executed. 

FR-9. The system shall accept signed integer READ values from -9999 through 9999. 

FR-10. The system shall reject READ input that is blank, non-integer, or outside the range of -9999 through 9999. 

FR-11. The system shall allow the user to correct and resubmit invalid READ input without restarting program execution. 

FR-12. The system shall display values produced by WRITE instructions in the Program output area. 

FR-13. The system shall display WRITE values using four-digit magnitude formatting with a separate negative sign for negative values. 

FR-14. The system shall preserve displayed program output after execution stops, completes, or encounters an error. 

FR-15. The system shall clear previous program output after a new program is successfully loaded. 


Non-Functional Requirements 

NFR-1. The system shall provide clearly labeled GUI controls so users can identify their purpose. 

NFR-2. The system shall keep user-interface code separate from the simulator's data model and business logic. 

NFR-3. The system shall remain responsive during program execution so the user can interact with controls such as Stop. 