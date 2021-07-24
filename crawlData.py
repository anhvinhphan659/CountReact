import requests

def getContentPage(url:str):
    req=requests.get(url=url)
    return req

def getReaction(content:str):
    edge_pos=content.find("top_reactions:{edges")
    res=[]
    if (edge_pos<0):
        return -1
    if(edge_pos>=0):
        main_content=content[edge_pos:]
        reacts=main_content.split("},")
        index=0
        while (reacts[index].find("reaction_count:")>=0 ):
            elements=reacts[index].split(",")
            num=elements[0].find("reaction_count:")
            num=elements[0][(num+len("reaction_count:")):]
            type=elements[-1].find("reaction_type:")
            if type<0:
                index+=1
                continue
            type=elements[-1][(type+len("reaction_type:")):]
            type=type.rstrip('"').lstrip('"')

            res.append((num,type))
            index+=1
        "hello".split()
        return res