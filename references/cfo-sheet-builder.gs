// Jarvis CFO Sheet Builder
// Paste this into Extensions > Apps Script > Run
// Builds TRANSACTIONS, P&L DASHBOARD, and TEAM COSTS tabs automatically

function buildCFOSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  // ─────────────────────────────────────────
  // TAB 1: TRANSACTIONS
  // ─────────────────────────────────────────
  var txTab = ss.getSheetByName("TRANSACTIONS");
  if (txTab) ss.deleteSheet(txTab);
  txTab = ss.insertSheet("TRANSACTIONS");

  // Headers
  var txHeaders = ["Date", "Description", "Category", "Type", "Amount ($)", "Running Balance ($)"];
  txTab.getRange(1, 1, 1, txHeaders.length).setValues([txHeaders]);
  txTab.getRange(1, 1, 1, txHeaders.length)
    .setBackground("#1a1a2e")
    .setFontColor("#ffffff")
    .setFontWeight("bold")
    .setFontSize(11);

  // Opening balance row
  txTab.getRange(2, 1).setValue(new Date());
  txTab.getRange(2, 2).setValue("Opening Balance");
  txTab.getRange(2, 3).setValue("—");
  txTab.getRange(2, 4).setValue("IN");
  txTab.getRange(2, 5).setValue(0);
  txTab.getRange(2, 6).setValue(0); // User fills this with Chase balance
  txTab.getRange(2, 6).setNote("Enter your current Chase balance here");
  txTab.getRange(2, 6).setBackground("#fff3cd");

  // Running balance formula for rows 3 onward (pre-fill 200 rows)
  for (var i = 3; i <= 200; i++) {
    txTab.getRange(i, 6).setFormula(
      "=IF(E" + i + "=\"\",F" + (i-1) + ",F" + (i-1) + "+IF(D" + i + "=\"IN\",E" + i + ",-E" + i + "))"
    );
  }

  // Category dropdown
  var categories = [
    "Revenue: Client Payment",
    "Revenue: Content Collab",
    "Revenue: HerFIT",
    "Expense: Payroll",
    "Expense: Meta Ads",
    "Expense: VA Cost",
    "Expense: Software/Tools",
    "Expense: Misc"
  ];
  var catRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(categories, true)
    .setAllowInvalid(false)
    .build();
  txTab.getRange(3, 3, 198, 1).setDataValidation(catRule);

  // Type dropdown
  var typeRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["IN", "OUT"], true)
    .setAllowInvalid(false)
    .build();
  txTab.getRange(3, 4, 198, 1).setDataValidation(typeRule);

  // Date format
  txTab.getRange(2, 1, 199, 1).setNumberFormat("yyyy-mm-dd");

  // Currency format
  txTab.getRange(2, 5, 199, 2).setNumberFormat("$#,##0.00");

  // Column widths
  txTab.setColumnWidth(1, 110);
  txTab.setColumnWidth(2, 250);
  txTab.setColumnWidth(3, 220);
  txTab.setColumnWidth(4, 70);
  txTab.setColumnWidth(5, 120);
  txTab.setColumnWidth(6, 160);

  // Freeze header
  txTab.setFrozenRows(1);

  // Alternating row colors
  txTab.getRange(2, 1, 199, 6).applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY);


  // ─────────────────────────────────────────
  // TAB 2: TEAM COSTS
  // ─────────────────────────────────────────
  var teamTab = ss.getSheetByName("TEAM COSTS");
  if (teamTab) ss.deleteSheet(teamTab);
  teamTab = ss.insertSheet("TEAM COSTS");

  var teamHeaders = ["Name", "Role", "Monthly Cost ($)", "Active?", "Notes"];
  teamTab.getRange(1, 1, 1, teamHeaders.length).setValues([teamHeaders]);
  teamTab.getRange(1, 1, 1, teamHeaders.length)
    .setBackground("#1a1a2e")
    .setFontColor("#ffffff")
    .setFontWeight("bold")
    .setFontSize(11);

  var teamData = [
    ["George", "Sales — Closer", "", "YES", "Commission-based"],
    ["Ruth", "Client Success", "", "YES", ""],
    ["Kamille", "Content / Creator Outreach", "", "YES", ""],
    ["JC", "Tech / Website", "", "YES", "As needed"],
    ["Sue", "Hiring / Talent", "", "YES", "As needed"],
    ["New SDR", "Appointment Setter", "", "YES", "Replacing Shemily"],
  ];
  teamTab.getRange(2, 1, teamData.length, teamData[0].length).setValues(teamData);

  // Active dropdown
  var activeRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["YES", "NO"], true)
    .build();
  teamTab.getRange(2, 4, 20, 1).setDataValidation(activeRule);

  // Currency
  teamTab.getRange(2, 3, 20, 1).setNumberFormat("$#,##0.00");

  // Highlight cost column
  teamTab.getRange(2, 3, teamData.length, 1).setBackground("#fff3cd");
  teamTab.getRange(1, 3).setNote("Fill in monthly cost per person");

  // Total row
  var totalRow = teamData.length + 2;
  teamTab.getRange(totalRow, 2).setValue("TOTAL MONTHLY PAYROLL");
  teamTab.getRange(totalRow, 2).setFontWeight("bold");
  teamTab.getRange(totalRow, 3).setFormula("=SUMIF(D2:D" + (totalRow-1) + ",\"YES\",C2:C" + (totalRow-1) + ")");
  teamTab.getRange(totalRow, 3).setFontWeight("bold").setNumberFormat("$#,##0.00").setBackground("#d4edda");

  // Column widths
  teamTab.setColumnWidth(1, 150);
  teamTab.setColumnWidth(2, 230);
  teamTab.setColumnWidth(3, 160);
  teamTab.setColumnWidth(4, 90);
  teamTab.setColumnWidth(5, 200);
  teamTab.setFrozenRows(1);


  // ─────────────────────────────────────────
  // TAB 3: P&L DASHBOARD
  // ─────────────────────────────────────────
  var plTab = ss.getSheetByName("P&L DASHBOARD");
  if (plTab) ss.deleteSheet(plTab);
  plTab = ss.insertSheet("P&L DASHBOARD", 0); // First tab

  // Title
  plTab.getRange("A1").setValue("💰 JARVIS CFO DASHBOARD");
  plTab.getRange("A1").setFontSize(18).setFontWeight("bold").setFontColor("#1a1a2e");
  plTab.getRange("A1:F1").merge();

  // Month selector
  plTab.getRange("A3").setValue("Month:");
  plTab.getRange("A3").setFontWeight("bold");
  plTab.getRange("B3").setFormula('=TEXT(TODAY(),"YYYY-MM")');
  plTab.getRange("B3").setBackground("#fff3cd").setFontWeight("bold");
  plTab.getRange("B3").setNote("Change this to view a different month e.g. 2026-03");

  // ── REVENUE SECTION ──
  plTab.getRange("A5").setValue("REVENUE");
  plTab.getRange("A5").setFontWeight("bold").setFontSize(12).setBackground("#d4edda");
  plTab.getRange("A5:C5").merge().setBackground("#d4edda");

  var revRows = [
    ["Client Payments (Jarvis)", '=SUMPRODUCT((TEXT(TRANSACTIONS!A:A,"YYYY-MM")=B3)*(TRANSACTIONS!C:C="Revenue: Client Payment")*(TRANSACTIONS!D:D="IN")*TRANSACTIONS!E:E)'],
    ["Content Collabs (@passionya)", '=SUMPRODUCT((TEXT(TRANSACTIONS!A:A,"YYYY-MM")=B3)*(TRANSACTIONS!C:C="Revenue: Content Collab")*(TRANSACTIONS!D:D="IN")*TRANSACTIONS!E:E)'],
    ["HerFIT", '=SUMPRODUCT((TEXT(TRANSACTIONS!A:A,"YYYY-MM")=B3)*(TRANSACTIONS!C:C="Revenue: HerFIT")*(TRANSACTIONS!D:D="IN")*TRANSACTIONS!E:E)'],
  ];
  for (var r = 0; r < revRows.length; r++) {
    plTab.getRange(6 + r, 1).setValue(revRows[r][0]);
    plTab.getRange(6 + r, 2).setFormula(revRows[r][1]);
    plTab.getRange(6 + r, 2).setNumberFormat("$#,##0.00");
  }

  // Total Revenue
  plTab.getRange("A9").setValue("TOTAL REVENUE");
  plTab.getRange("A9").setFontWeight("bold");
  plTab.getRange("B9").setFormula("=SUM(B6:B8)");
  plTab.getRange("B9").setFontWeight("bold").setNumberFormat("$#,##0.00").setBackground("#d4edda");

  // ── EXPENSES SECTION ──
  plTab.getRange("A11").setValue("EXPENSES");
  plTab.getRange("A11").setFontWeight("bold").setFontSize(12);
  plTab.getRange("A11:C11").merge().setBackground("#f8d7da");

  var expRows = [
    ["Payroll", '=SUMPRODUCT((TEXT(TRANSACTIONS!A:A,"YYYY-MM")=B3)*(TRANSACTIONS!C:C="Expense: Payroll")*(TRANSACTIONS!D:D="OUT")*TRANSACTIONS!E:E)'],
    ["Meta Ads", '=SUMPRODUCT((TEXT(TRANSACTIONS!A:A,"YYYY-MM")=B3)*(TRANSACTIONS!C:C="Expense: Meta Ads")*(TRANSACTIONS!D:D="OUT")*TRANSACTIONS!E:E)'],
    ["VA Cost", '=SUMPRODUCT((TEXT(TRANSACTIONS!A:A,"YYYY-MM")=B3)*(TRANSACTIONS!C:C="Expense: VA Cost")*(TRANSACTIONS!D:D="OUT")*TRANSACTIONS!E:E)'],
    ["Software & Tools", '=SUMPRODUCT((TEXT(TRANSACTIONS!A:A,"YYYY-MM")=B3)*(TRANSACTIONS!C:C="Expense: Software/Tools")*(TRANSACTIONS!D:D="OUT")*TRANSACTIONS!E:E)'],
    ["Misc", '=SUMPRODUCT((TEXT(TRANSACTIONS!A:A,"YYYY-MM")=B3)*(TRANSACTIONS!C:C="Expense: Misc")*(TRANSACTIONS!D:D="OUT")*TRANSACTIONS!E:E)'],
  ];
  for (var e = 0; e < expRows.length; e++) {
    plTab.getRange(12 + e, 1).setValue(expRows[e][0]);
    plTab.getRange(12 + e, 2).setFormula(expRows[e][1]);
    plTab.getRange(12 + e, 2).setNumberFormat("$#,##0.00");
  }

  // Total Expenses
  plTab.getRange("A17").setValue("TOTAL EXPENSES");
  plTab.getRange("A17").setFontWeight("bold");
  plTab.getRange("B17").setFormula("=SUM(B12:B16)");
  plTab.getRange("B17").setFontWeight("bold").setNumberFormat("$#,##0.00").setBackground("#f8d7da");

  // ── SUMMARY SECTION ──
  plTab.getRange("A19").setValue("SUMMARY");
  plTab.getRange("A19").setFontWeight("bold").setFontSize(12);
  plTab.getRange("A19:C19").merge().setBackground("#cce5ff");

  var summaryRows = [
    ["Net Profit / Loss", "=B9-B17"],
    ["Profit Margin", "=IFERROR(B20/B9,0)"],
    ["Chase Balance (manual)", ""],
    ["Months of Runway", "=IFERROR(B22/B17,0)"],
    ["Status", '=IF(B21>0.4,"✅ Healthy — Keep scaling",IF(B21>0.2,"⚠️ Watch it — margins tightening",IF(B21>0,"🔴 Tight — cut expenses now","🚨 Losing Money — emergency")))'],
  ];

  for (var s = 0; s < summaryRows.length; s++) {
    plTab.getRange(20 + s, 1).setValue(summaryRows[s][0]);
    if (summaryRows[s][1]) {
      plTab.getRange(20 + s, 2).setFormula(summaryRows[s][1]);
    }
  }

  // Formatting for summary
  plTab.getRange("B20").setNumberFormat("$#,##0.00").setFontWeight("bold");
  plTab.getRange("B21").setNumberFormat("0.0%").setFontWeight("bold");
  plTab.getRange("B22").setNumberFormat("$#,##0.00").setBackground("#fff3cd").setNote("Update this manually from Chase screenshot");
  plTab.getRange("B23").setNumberFormat("0.0").setFontWeight("bold");
  plTab.getRange("B24").setFontWeight("bold").setFontSize(12).setBackground("#cce5ff");

  // Conditional color on net profit
  plTab.getRange("B20").setBackground("#d4edda");

  // Column widths
  plTab.setColumnWidth(1, 220);
  plTab.setColumnWidth(2, 160);
  plTab.setColumnWidth(3, 160);

  // Freeze
  plTab.setFrozenRows(1);

  // ─────────────────────────────────────────
  // REORDER TABS
  // ─────────────────────────────────────────
  ss.setActiveSheet(plTab);
  ss.moveActiveSheet(1);

  SpreadsheetApp.getUi().alert("✅ CFO Sheet built successfully!\n\nNext steps:\n1. Fill in team costs in TEAM COSTS tab\n2. Enter your Chase balance in TRANSACTIONS row 2, column F\n3. Screenshot Chase and send to Claude — he'll give you rows to paste");
}
