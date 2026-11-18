import math
def compare(rows):
    groups={}
    for row in rows:
        b=groups.setdefault(row['route'],{'n':0,'passed':0,'seconds':0.0,'cost':0.0})
        b['n']+=1;b['passed']+=bool(row['passed']);b['seconds']+=float(row['seconds']);b['cost']+=float(row['cost_usd'])
    return {key:{'n':b['n'],'pass_rate':b['passed']/b['n'],'mean_seconds':math.fsum(float(r['seconds']) for r in rows if r['route']==key)/b['n'],'mean_cost_usd':math.fsum(float(r['cost_usd']) for r in rows if r['route']==key)/b['n']} for key,b in groups.items()}
