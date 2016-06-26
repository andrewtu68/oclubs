import MySQLdb
db = MySQLdb.connect(host="localhost", user="root", db="oclubs")
cur = db.cursor()

# cond: a tuple, like: "=","user_id",self.uid
# for range: lower bound included, higher bound excluded


def cond_interpret(cond):
    if cond[0] in ['>', '<', '=', '<=', '>=', '<>']:
        if isinstance(cond[2], basestring):
            return cond[1] + cond[0]+"\""+cond[2]+"\""
        else:
            return cond[1] + cond[0]+str(cond[2])
    elif cond[0] == "range":
        if not (isinstance(cond[2][0], int) or isinstance(cond[2][0], float)):
            raise RuntimeError
        if not (isinstance(cond[2][1], int) or isinstance(cond[2][1], float)):
            raise RuntimeError
        return cond[1]+'>='+cond[2][0]+" AND " + cond[1]+'<'+cond[2][1]


def fetch_onerow(table, conds, coldict, isand=True):
    cols = coldict.keys()
    st = ','.join(cols)
    fconds = []
    for cond in conds:
        fconds.append(cond_interpret(cond))
    if isand:
        fconds = " AND ".join(fconds)
    else:
        fconds = " OR ".join(fconds)
    cur.execute("SELECT %s FROM %s WHERE %s LIMIT 1" % (st, table, fconds))
    read = cur.fetchall()
    if len(read) == 0:
        return None
    ret = {}
    ret.fromkeys(coldict.values())
    i = 0
    for val in read[0]:
        ret[coldict[cols[i]]] = val
        i += 1
    return ret


def fetch_oneblock(table, conds, col, isand=True):
    fconds = []
    for cond in conds:
        fconds.append(cond_interpret(cond))
    if isand:
        fconds = " AND ".join(fconds)
    else:
        fconds = " OR ".join(fconds)
    cur.execute("SELECT %s FROM %s WHERE %s LIMIT 1" % (col, table, fconds))
    read = cur.fetchall()
    if len(read) == 0:
        return None
    return read[0][0]


def fetch_allrow(table, conds, coldict, isand=True):
    cols = coldict.keys()
    st = ','.join(cols)
    fconds = []
    for cond in conds:
        fconds.append(cond_interpret(cond))
    if isand:
        fconds = " AND ".join(fconds)
    else:
        fconds = " OR ".join(fconds)
    cur.execute("SELECT %s FROM %s WHERE %s" % (st, table, fconds))
    reads = cur.fetchall()
    if len(reads) == 0:
        return None
    rows = []
    for read in reads:
        row = {}
        row.fromkeys(coldict.values)
        i = 0
        for val in read:
            row[coldict[cols[i]]] = val
            i += 1
        rows.append(row)
    return rows