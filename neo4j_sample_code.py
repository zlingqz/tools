
from py2neo import Graph,Node,Relationship, NodeMatcher, RelationshipMatcher, Path


class Social():
    def __init__(self, host, user, password):
        # 连接neo4j数据库，输入地址、用户名、密码
        self.graph = Graph(host, auth=(user, password))

    def nodeParser(self, node):
        """解析出节点，返回节点label及所有的属性，以字典形式返回"""
        nodeValues = dict(node)
        nodeLabels = list(node.labels)
        nodeValues["label"] = nodeLabels
        return nodeValues

    def relationParse(self,rel):
        relations = dict(rel)
        relations["type"] = type(rel).__name__
        relations["startNode"] = rel.start_node["id"]
        relations["endNode"] = rel.end_node["id"]
        return relations

    def postMatch(self):
        """查询所有帖子"""
        posts = []
        query = "MATCH (p:post) return p limit 3"
        result = self.graph.run(query).data()
        for p in result:
            posts.append(self.nodeParser(p['p']))
        return posts

    def userComUser(self, userid):
        query = "MATCH p=(:USER {userID: 'USER_%s'} )-->(:post) <-- (:comment) <-- (:USER) RETURN p" % (userid)
        try:
            result = self.graph.run(query).data()
        except:
            return -1
        for i, path in enumerate(result):
            for k, v in path.items():
                print(v.nodes[3])
                comUser = self.nodeParser(v.nodes[3])
                print(comUser)
            break

if __name__ == '__main__':
    host = "bolt://192.168.0.101:7687"
    user = "neo4j"
    password = "neo4j"
    soc = Social(host,user,password)
    #soc.userComUser('1044836695055699969')
    soc.postMatch()
