import uuid

num_items = 1000

num_servers = 50
delta_servers = +1
points_per_server = 100

num_runs = 5
verbose = False


def produce_values(num_items=num_items):
    """Produce integers to represent actual items"""
    items = [uuid.uuid4().int
                 for i in range(num_items)]
    return items
    
def naive_hashing(items, num_servers):
    """naive_hashing"""
    return [i % num_servers for i in items]

def consistent_hashing(items, num_servers, server_hashes):
    """consistent hashing. Terribly inefficient, but good enough for now"""

    def get_server(item, server_hashes):
        # print(item)
        try:
            return next( server for (hash, server) in server_hashes
                      if hash >= item)
        except Exception:
            return -1
        
    return [ get_server(i, server_hashes)
                for i in items]

    
def num_rehashes(old, new):
    return [not o == n for o, n in zip(old, new)]

def server_hashes(num_servers, points_per_server=points_per_server):
    # tmp = [
    #     [(uuid.uuid4().int, s) for n in range(num_servers)]
    #     for s in range(num_servers)]

    # print ("server_hashes num_servers", num_servers)
    tmp = [[(uuid.uuid4().int, s)
               for n in range(points_per_server)]
               for s in range(num_servers)]
    return tmp

def flatten_hashes(num_servers, server_hashes):
    """use only some of the server hashes"""

    tmp = server_hashes[:num_servers]
    
    # flatten:
    tmp = [item for sublist in tmp for item in sublist]
    tmp.sort()
    # print("flattened:", num_servers, tmp)

    return tmp 

if __name__ == "__main__":
    
    for i in range(num_runs):
        items = produce_values()
        if verbose: 
            print(items)

        # naive hashing:

        before_servers = naive_hashing(items, num_servers)
        after_servers  = naive_hashing(items, num_servers+delta_servers)
        if verbose: 
            print(before_servers)
            print(after_servers)

        naive_rehashes = sum(num_rehashes(before_servers, after_servers))
        print("N", naive_rehashes)

        # consistent hashing: 
        sh = server_hashes(max(num_servers, num_servers+delta_servers))
        # print("All server hashes: ", sh)
        
        before_servers = consistent_hashing(
            items, num_servers,
            flatten_hashes(num_servers, sh))
            
        after_servers  = consistent_hashing(
            items, num_servers+delta_servers,
            flatten_hashes(num_servers+delta_servers, sh))

        if verbose: 
            print(before_servers)
            print(after_servers)

        consistent_rehashes = sum(num_rehashes(before_servers, after_servers))
        print("C", consistent_rehashes)
