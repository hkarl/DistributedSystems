import uuid
import bisect

num = 15
num_servers = 4
xscale = 10.
points_per_server = 3
colors = ['red', 'green', 'blue', 'yellow', 'black']

# simple hashing:

uuids = [uuid.uuid4().int for i in range(num)]
servers = [ (x, x % num_servers, x % (num_servers +1)) for x in uuids]
# print(servers)

few_server_x = [s*(xscale/(num_servers-1)) for s in range(num_servers)]
more_server_x = [s*(xscale/(num_servers)) for s in range(num_servers+1)]

print("\\begin{tikzpicture}")
print ("\\draw [thin] (0,0) -- ({},0);".format(xscale)) 
for s in range(num_servers):
    print("\\node at ({}, 1) {{S{}}};".format(few_server_x[s], s))
for s in range(num_servers+1):
    print("\\node at ({}, -1) {{S{}}};".format(more_server_x[s], s))
    
for s in servers:
    x = (float(s[0]) / 2**128 * xscale)
    # print("\\draw [thick] ({},0) -- ({},1);".format(x, x))
    print("\\node at  ({},0) {{X}};".format(x, x))
    print("\\draw ({}, 0.2) -- ({}, 0.8);".format(x, few_server_x[s[1]]))

    if s[1] == s[2]: 
        print("\\draw ({},-0.2) -- ({}, -0.8);".format(x, more_server_x[s[2]]))
    else:
        print("\\draw[red] ({},-0.2) -- ({}, -0.8);".format(x, more_server_x[s[2]]))
        
print("\\end{tikzpicture}")


print ("%--------------")

# consistent hashing
print("\\begin{tikzpicture}")


server_points =  [[(uuid.uuid4().int, s)
               for n in range(points_per_server)]
               for s in range(num_servers)]

# print(server_points)

all_points = sorted([item for sublist in server_points for item in sublist],
                        key= lambda x:x[0])

# print(all_points)

def consistent_hashing(items, server_hashes):
    def get_server(item, server_hashes):
        return bisect.bisect(hashes, item) 

    hashes = [x[0] for x in server_hashes]
    return [get_server(i, hashes) for i in items]


def uuid2angle(uuid):
    return int(float(uuid)/float(2**128)*360)

indexes = consistent_hashing(uuids, all_points)
# print(indexes)

for a, aprime in zip(all_points[:-1], all_points[1:]) :
    start = uuid2angle(a[0])
    end = uuid2angle(aprime[0])
    # print(start, end, colors[a[1]])
    print("\\draw[fill={color}] ({start}:1cm) arc [start angle = {start}, end angle={end}, radius=1cm] --++({end}:1cm) arc  [start angle = {end}, end angle={start}, radius=2cm] --++({start}:-1cm)--cycle;".format(color=colors[a[1]], start=start, end=end))

# special case for first one:
end = uuid2angle(all_points[-1][0]) -360
start = uuid2angle(all_points[0][0])
print("\\draw[fill={color}] ({start}:1cm) arc [start angle = {start}, end angle={end}, radius=1cm] --++({end}:1cm) arc  [start angle = {end}, end angle={start}, radius=2cm] --++({start}:-1cm)--cycle;".format(color=colors[all_points[-1][1]], start=start, end=end))
    

# Print the UUIDs

for u in uuids:
    print("\\node at ({{{}}}:1.5cm) {{X}};".format(uuid2angle(u)))
    
print("\\end{tikzpicture}")


#############

num_servers = num_servers + 1
# consistent hashing
print("\\begin{tikzpicture}")

colors = ['red', 'green', 'blue', 'yellow', 'gray!10']

server_points =  server_points + [[(uuid.uuid4().int, num_servers-1)
                                   for n in range(points_per_server)]]




all_points = sorted([item for sublist in server_points for item in sublist],
                        key= lambda x:x[0])

# print(all_points)

def consistent_hashing(items, server_hashes):
    def get_server(item, server_hashes):
        return bisect.bisect(hashes, item) 

    hashes = [x[0] for x in server_hashes]
    return [get_server(i, hashes) for i in items]


def uuid2angle(uuid):
    return int(float(uuid)/float(2**128)*360)

indexes = consistent_hashing(uuids, all_points)
# print(indexes)

for a, aprime in zip(all_points[:-1], all_points[1:]) :
    start = uuid2angle(a[0])
    end = uuid2angle(aprime[0])
    # print(start, end, colors[a[1]])
    print("\\draw[fill={color}] ({start}:1cm) arc [start angle = {start}, end angle={end}, radius=1cm] --++({end}:1cm) arc  [start angle = {end}, end angle={start}, radius=2cm] --++({start}:-1cm)--cycle;".format(color=colors[a[1]], start=start, end=end))

# special case for first one:
end = uuid2angle(all_points[-1][0]) -360
start = uuid2angle(all_points[0][0])
print("\\draw[fill={color}] ({start}:1cm) arc [start angle = {start}, end angle={end}, radius=1cm] --++({end}:1cm) arc  [start angle = {end}, end angle={start}, radius=2cm] --++({start}:-1cm)--cycle;".format(color=colors[all_points[-1][1]], start=start, end=end))
    

# Print the UUIDs

for u in uuids:
    print("\\node at ({{{}}}:1.5cm) {{X}};".format(uuid2angle(u)))
    
print("\\end{tikzpicture}")
