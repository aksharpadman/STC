import math
import networkx as nx
import matplotlib.pyplot as plt

x = int(raw_input("no of nodes in the workspace (perfect square): "))
ques= str(raw_input("are there any obstacles? y or n: "))
if ques == "y":
	inp= raw_input("enter obstacle nodes with comma(nodes are numbered from 0): ") #nodes which are having obstacles or are out of the map
	input_list = inp.split(',') #telling the program to split the inputs in "inp" by commas
	l=[int(h.strip()) for h in input_list] #saving the obstacle node in list 'l'
elif ques == "n":
	l=[]

p=int((math.sqrt(x)+1)**2)

#function to form the edges list for the graph for agent path plan
def edges(n,l):
	lists=[]
	M = [[0 for x in range(n)] for y in range(n)]
	for i in range(n):
		for j in range(n):
			if i==j:
				M[i][j]=10
			elif i-j==1 or j-i==1:
				if i==0 or j==0:
					M[i][j]=1
				elif (i%math.sqrt(n)==0 and i>j) or (j%math.sqrt(n)==0 and j>i):
					M[i][j]=10
				else:
					M[i][j]=1
			elif i-j==math.sqrt(n) or j-i==math.sqrt(n):
				M[i][j]=1
			else:
				M[i][j]=10
	#print('\n\n'.join(['    '.join(['{:n}'.format(item) for item in row]) for row in M]))
	for i in range(n):
		c=[M[i][j] for j in range(n)]
		#k=min(c)
		for j in range(n):
			if M[i][j] ==1:
			
				M[j][i]=10
				#print i,j
				lists.append((i,j))
	v=[]    
	for i in l:#obstacle nodes and its edges are eliminated from the list       
		for each in lists:#edges having the obstacle node are removed using if condition
			if each[0]==i or each[1]==i:
				v.append(each)
        
	for each in v:
		if each in lists:
			lists.remove(each)        
	return lists#the function returns the workspace graph containing the edges

#edge list used only for the visual represenstation of the workspace
def edge(n):
    lists=[]
    M = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if i==j:
                M[i][j]=10
            elif i-j==1 or j-i==1:
                if i==0 or j==0:
                    M[i][j]=1
                elif (i%math.sqrt(n)==0 and i>j) or (j%math.sqrt(n)==0 and j>i):
                    M[i][j]=10
                else:
                    M[i][j]=1
            elif i-j==math.sqrt(n) or j-i==math.sqrt(n):
                M[i][j]=1
            else:
                M[i][j]=10
    for i in range(n):
        c=[M[i][j] for j in range(n)]
        for j in range(n):
            if M[i][j] ==1:
            
                M[j][i]=10
                
                lists.append((i,j))
    return lists#function to define the workspace
 
H=nx.Graph()#creates an empty graph for the path    
G=nx.Graph()#creates an empy graph for the workspace boundaries for visual representation
for i in range(x):#nodes with position are added to the empty graph
	a=int((i/math.sqrt(x)))+0.5#gives the x coordinate of the nodes
	b=int((i%math.sqrt(x)))+0.5#gives the y coordinate of the nodes
	G.add_node(i,pos=(a,b))#adds the node to the graph with its attribute/position


for i in range(p):#adds nodes with postion for the workspace boundaries for visual representation
	c=int((i/math.sqrt(p)))
	d=int((i%math.sqrt(p)))
	H.add_node(i,pos=(c,d))

G.add_edges_from(edges(x,l))#adds the edges to the graph using the edge function
H.add_edges_from(edge(p))#adds the edges to the boundary graph 

nx.draw_networkx_edges(H,nx.get_node_attributes(H, 'pos'),edgelist=H.edges(),width=3)
nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=0)

T=nx.minimum_spanning_tree(G)#constructs a spanning tree of the graph G
nx.draw_networkx_nodes(G,nx.get_node_attributes(G, 'pos'),nodelist=T.nodes(),node_color='r')#constructs thenodes of the graph G
nx.draw_networkx_edges(G,nx.get_node_attributes(G, 'pos'),edgelist=T.edges(),edge_color='r',width=3)#constructs the edges of the graph G

#assuming the initial position and the previous position of the robot
cur_pos=[0.25,0.25]
prev_pos=[0.25,0.75]


def get_cur_dir(cur_pos, prev_pos):#present direction of the bot
        right=1
        up=2
        left=3
        down=4
        x=cur_pos[0]-prev_pos[0]#difference of cur. x coord and prev coord gives left or right
        y=cur_pos[1]-prev_pos[1]# up or down
        if(x>0):
            return right
        if(x<0):
            return left
        if(x==0):
            if(y>0):
                return up
            else:
                return down

def get_cur_node(cur_pos):#finding current minor node
    dec_part=[cur_pos[0]-int(cur_pos[0]), cur_pos[1]-int(cur_pos[1])]
    int_part=[cur_pos[0]-dec_part[0], cur_pos[1]-dec_part[1]]
    node_pos=[]
    for each in dec_part:
        if each == .25:
            node_pos.append(each+.25)
        else:
            node_pos.append(each-.25)
    node_pos[0]+=int_part[0]
    node_pos[1]+=int_part[1]
    node_pos=tuple(node_pos)
    for each in G.nodes(data=True):
        if each[1]['pos']==node_pos:
            return each[0]  

def get_block_list(T, cur_node):#finding tree branches in the curr node
    cur_pos=list(T.nodes(data=True)[cur_node][1]['pos'])
    ns=T.neighbors(cur_node)
    ret_list=[]
    for each in ns:
        ns_pos=list(T.nodes(data=True)[each][1]['pos'])
        x=cur_pos[0]-ns_pos[0]
        y=cur_pos[1]-ns_pos[1]
        if(x>0):
            ret_list.append(3)
        if(x<0):
            ret_list.append(1)
        if(x==0):
            if(y>0):
                ret_list.append(4)
            else:
                ret_list.append(2)
    return ret_list

def get_quadrant(cur_pos):
    x=cur_pos[0]
    y=cur_pos[1]
    p=x-int(x)
    q=y-int(y)
    if p==.25 and q==.25:
        return 4
    if p==.25 and q==.75:
        return 3
    if p==.75 and q==.75:
        return 2
    if p==.75 and q==.25:
        return 1

def get_moving_dir(cur_dir, block_list, cur_quadrant):
    b=cur_dir
    a=cur_quadrant
    c=block_list
    if a==b:
        if a not in c:
            return a+1
        else:
            return a
    if a!=b:
        if a not in c:
            return a+1
        else:
            return a

def get_path(cur_pos, prev_pos, T):
    ret_path=[]
    ret_pat=[]
    initial_pos=list(cur_pos)
    i=1
    while(cur_pos!=prev_pos):
        
        if i!=1:
            if cur_pos==initial_pos:
                break
        
        cur_dir=get_cur_dir(cur_pos,prev_pos)
        cur_node=get_cur_node(cur_pos)
        block_list=get_block_list(T, cur_node)
        cur_quadrant=get_quadrant(cur_pos)
        mov_dir=get_moving_dir(cur_dir,block_list,cur_quadrant)
        prev_pos=list(cur_pos)
        if mov_dir==1 or mov_dir==5:
            cur_pos[0]=cur_pos[0]+0.5
            cur_pos[1]=cur_pos[1]
        if mov_dir==2:
            cur_pos[0]=cur_pos[0]
            cur_pos[1]=cur_pos[1]+0.5
        if mov_dir==3:
            cur_pos[0]=cur_pos[0]-0.5
            cur_pos[1]=cur_pos[1]
        if mov_dir==4 or mov_dir==0:
            cur_pos[0]=cur_pos[0]
            cur_pos[1]=cur_pos[1]-0.5            
        i=i+1            
        ret_pat.append([tuple(prev_pos), tuple(cur_pos)])
    return ret_pat

h=get_path(cur_pos, prev_pos, T)#builds the tree for the path for the robot

#code to visually represent the path of the robot
path_node=[]
j=[]
F=nx.Graph()
k=[]
# print len(h)
for i in range(len(h)):
    k.append(h[i][1])
    F.add_node(i,pos=k[i])
    path_node.append(i)
for i in range(len(h)-1):
    j.append((i,i+1))

F.add_edges_from(j)
nx.draw(F, nx.get_node_attributes(F, 'pos'), with_labels=True, node_size=0)
nx.draw_networkx_edges(F,nx.get_node_attributes(F, 'pos'),edgelist=F.edges(),edge_color='g',width=2)

plt.show()


