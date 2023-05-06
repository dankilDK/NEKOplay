def cmp(a, b):
  return a.count(' ') > b.count(' ')

def merge(a, b):
    res = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if cmp(a[i], b[j]):
            res.append(a[i])
            i += 1
        else:
           res.append(b[j])
           j += 1
    res.extend(a[i:])
    res.extend(b[j:])
    return res
  

def msort(a):
  if len(a) <= 1:
    return a
  k = len(a) // 2
  return merge(msort(a[:k]), msort(a[k:]))
