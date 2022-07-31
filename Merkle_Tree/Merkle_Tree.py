import hashlib
import time


class MerkleNode(object):
    def __init__(self,left=None,right=None,data=None):
        self.left = left
        self.right = right
        self.data = data

def createTree(nodes):
    list_len = len(nodes)
    if list_len == 0:
        return 0
    else:
        while list_len %2 != 0:
            nodes.extend(nodes[-1:])
            list_len = len(nodes)
        secondary = []
        for k in [nodes[x:x+2] for x in range(0,list_len,2)]:
            d1 = k[0].data.encode()
            d2 = k[1].data.encode()
            md5 = hashlib.md5()
            md5.update(d1+d2)
            newdata = md5.hexdigest()
            node = MerkleNode(left=k[0],right=k[1],data=newdata)
            secondary.append(node)
        if len(secondary) == 1:
            return secondary[0]
        else:
            return createTree(secondary)
def dfs(root):
    if  root != None:
        print("data:",root.data)
        dfs(root.left)
        dfs(root.right)
def bfs(root):
    print('开始遍历树')
    queue = []
    queue.append(root)
    while(len(queue)>0):
        e = queue.pop(0)
        print(e.data)
        if e.left != None:
            queue.append(e.left)
        if e.right != None:
            queue.append(e.right)

def Merkle_Tree(blocks):
    print('开始创建树')
    nodes = []
    for e in blocks:
        md5 = hashlib.md5()
        md5.update(e.encode())
        d=md5.hexdigest()
        nodes.append(MerkleNode(data=d))
    root = createTree(nodes)
    bfs(root)
    return nodes

if __name__ == "__main__":
    
    time_start = time.time()
    Merkle_Tree(['A','B','C','D','E'] )
    time_end = time.time()
    time_c = time_end - time_start
    print('耗时', time_c, 's')