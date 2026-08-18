"""Generate synthetic Planview-like data for the GCP AI demo kit.

This data is NOT FedEx data and does not represent the FedEx Planview operating model.
It is intentionally simplified for architecture/demo purposes.
"""
from pathlib import Path
import csv, json, random, datetime

OUT = Path(__file__).parent
random.seed(42)

portfolios = [
    ("PF-100", "Network Modernization", "Technology"),
    ("PF-200", "Operational Excellence", "Operations"),
    ("PF-300", "Customer Experience", "Commercial"),
]
programs = []
projects = []
for p_id, p_name, org in portfolios:
    for i in range(1, 4):
        prg_id = f"PG-{p_id[-3:]}-{i:02d}"
        programs.append((prg_id, f"{p_name} Program {i}", p_id))
        for j in range(1, 6):
            project_id = f"PJ-{p_id[-3:]}-{i:02d}-{j:02d}"
            projects.append((project_id, f"{p_name} Project {i}.{j}", prg_id, random.choice(["Green","Yellow","Red"]), random.choice(["Plan","Build","Validate","Deploy"])))

owners = ["A. Smith", "M. Chen", "R. Patel", "S. Jones", "L. Brown", "K. Davis"]
log_types = ["Risk", "Issue", "Decision", "Dependency", "Assumption"]
statuses = ["Open", "In Review", "Mitigated", "Closed", "Blocked"]

# Project master
with open(OUT/'planview_project.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['project_id','project_name','program_id','health','phase','owner'])
    for project in projects:
        w.writerow([*project, random.choice(owners)])

with open(OUT/'planview_portfolio.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['portfolio_id','portfolio_name','business_area'])
    w.writerows(portfolios)

with open(OUT/'planview_program.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['program_id','program_name','portfolio_id'])
    w.writerows(programs)

# Financials
with open(OUT/'planview_financial.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['project_id','fiscal_year','fiscal_month','budget_amount','forecast_amount','actual_amount','capex_opex'])
    for pid, *_ in projects:
        base = random.randint(500000, 4500000)
        for m in range(1,13):
            budget = base/12 * random.uniform(.85,1.15)
            forecast = budget * random.uniform(.88,1.25)
            actual = forecast * random.uniform(.75,1.10)
            w.writerow([pid, 2027, m, round(budget,2), round(forecast,2), round(actual,2), random.choice(['CAPEX','OPEX'])])

# Logbook CSV and raw JSON sample
log_records=[]
start=datetime.date(2026,1,1)
for i in range(1,801):
    pid=random.choice(projects)[0]
    cdate=start+datetime.timedelta(days=random.randint(0,240))
    status=random.choice(statuses)
    rdate=None if status in ['Open','In Review','Blocked'] else cdate+datetime.timedelta(days=random.randint(1,45))
    rec={
        'logbookId': f'LB-{i:05d}',
        'projectId': pid,
        'logType': random.choice(log_types),
        'logStatus': status,
        'severity': random.choice(['Low','Medium','High','Critical']),
        'ownerName': random.choice(owners),
        'createdDate': cdate.isoformat(),
        'resolvedDate': rdate.isoformat() if rdate else '',
        'summaryText': random.choice([
            'Vendor dependency may impact release schedule',
            'Data mapping requires architecture decision',
            'Budget variance requires follow-up with finance',
            'Security review pending for integration approach',
            'Implementation team blocked by missing requirement',
            'Change request approved by steering group',
        ]),
        'sourceSystem': 'SyntheticPlanview'
    }
    log_records.append(rec)
with open(OUT/'planview_logbook.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(log_records[0].keys())); w.writeheader(); w.writerows(log_records)
with open(OUT/'raw_logbook_sample.json','w') as f:
    json.dump(log_records[:20],f,indent=2)

# AgilePlace-style execution
with open(OUT/'agileplace_work_item.csv','w',newline='') as f:
    cols=['work_item_id','project_id','parent_work_item_id','work_item_type','title','state','blocked_flag','created_date','closed_date','story_points']
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    ctr=1
    for pid,*_ in projects:
        epics=[]
        for e in range(1,4):
            eid=f'WI-{ctr:06d}'; ctr+=1; epics.append(eid)
            w.writerow({'work_item_id':eid,'project_id':pid,'parent_work_item_id':'','work_item_type':'Epic','title':f'Epic {e} for {pid}','state':random.choice(['Backlog','In Progress','Done']),'blocked_flag':False,'created_date':'2026-01-15','closed_date':'','story_points':''})
        for s in range(1,16):
            created=start+datetime.timedelta(days=random.randint(0,240))
            state=random.choice(['Backlog','Ready','In Progress','Review','Done','Blocked'])
            closed='' if state not in ['Done'] else (created+datetime.timedelta(days=random.randint(3,45))).isoformat()
            w.writerow({'work_item_id':f'WI-{ctr:06d}','project_id':pid,'parent_work_item_id':random.choice(epics),'work_item_type':'Story','title':f'Story {s} for {pid}','state':state,'blocked_flag':state=='Blocked','created_date':created.isoformat(),'closed_date':closed,'story_points':random.choice([1,2,3,5,8,13])}); ctr+=1

# OKR synthetic
with open(OUT/'planview_okr.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['objective_id','portfolio_id','objective_name','key_result','target_value','current_value','status'])
    c=1
    for pf, pname, _ in portfolios:
        for k in range(1,4):
            target=100; current=random.randint(30,105)
            w.writerow([f'OKR-{c:04d}', pf, f'Improve {pname} outcome {k}', f'KR {k}: achieve measurable improvement', target, current, random.choice(['On Track','At Risk','Off Track'])]); c+=1

print(f'Generated data in {OUT}')
