import graphene
import pymongo

mongoURI = '{0}://{1}:{2}@{3}'.format("mongodb", "root", "31415926", "139.59.214.28:27017",)

class Episode(graphene.Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6

class Character(graphene.Interface):
    id = graphene.ID()
    name = graphene.String()
    friends = graphene.List(lambda: Character)
    appears_in = graphene.List(Episode)

    def resolve_friends(self, info):
        # The character friends is a list of strings
        # return [get_character(f) for f in self.friends]
        pass

class Human(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    home_planet = graphene.String()


class Droid(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    primary_function = graphene.String()

class Time(graphene.ObjectType):
    name = graphene.String()
    values = graphene.List(graphene.Float)
    units = graphene.String()
    dimensions = graphene.List(graphene.String)
    indexes = graphene.List(graphene.Int)

class Pres(graphene.ObjectType):
    name = graphene.String()
    values = graphene.List(graphene.List(graphene.Float))
    units = graphene.String()
    dimensions = graphene.List(graphene.String)

# class People(graphene.ObjectType):
#     name = graphene.String
#     age = graphene.Int


class Query(graphene.ObjectType):
    time = graphene.Field(Time, dataSet=graphene.String(default_value=""), gt=graphene.Float(), gte=graphene.Float(), lt=graphene.Float(), lte=graphene.Float(), eq=graphene.Float())
    pres = graphene.Field(Pres, dataSet=graphene.String(default_value=""), time=graphene.String())
    human = graphene.Field(Human,)


    def resolve_time(self, info, **args):
        print(info.field_asts)
        print(args)
        # print(lt)
        # print(eq)
        client = pymongo.MongoClient(mongoURI)
        db = client[args.get('dataSet')]
        coll = db["TIME"]

        f = {}
        s = {}
        doc = coll.find_one()
        vals = doc["values"]
        idxs_l = range(len(doc["values"]))
        print(idxs_l)
        if args.get("gt") != None or args.get("gte") != None:
            if args.get("gte") == None:
                res = []
                idxs = []
                for i, item in enumerate(vals):
                    if item > args.get("gt"):
                        res.append(item)
                        idxs.append(idxs_l[i])
                vals = res
                idxs_l = idxs
            elif args.get("gt") == None:
                res = []
                idxs = []
                for i, item in enumerate(vals):
                    if item >= args.get("gte"):
                        res.append(item)
                        idxs.append(idxs_l[i])
                vals = res
                idxs_l = idxs
            else:
                if args.get("gt")>= args.get("gte"):
                    res = []
                    idxs = []
                    for i, item in enumerate(vals):
                        if item > args.get("gt"):
                            res.append(item)
                            idxs.append(idxs_l[i])
                    vals = res
                    idxs_l = idxs
                else:
                    res = []
                    idxs = []
                    for i, item in enumerate(vals):
                        if item >= args.get("gte"):
                            res.append(item)
                            idxs.append(idxs_l[i])
                    vals = res
                    idxs_l = idxs
        if args.get("lt") != None or args.get("lte") != None:
            if args.get("lte") == None:
                res = []
                idxs = []
                for i, item in enumerate(vals):
                    if item < args.get("lt"):
                        res.append(item)
                        idxs.append(idxs_l[i])
                vals = res
                idxs_l = idxs
            elif args.get("lt") == None:
                res = []
                idxs = []
                for i, item in enumerate(vals):
                    if item <= args.get("lte"):
                        res.append(item)
                        idxs.append(idxs_l[i])
                vals = res
                idxs_l = idxs
            else:
                if args.get("lt")<= args.get("lte"):
                    res = []
                    idxs = []
                    for i, item in enumerate(vals):
                        if item < args.get("lt"):
                            res.append(item)
                            idxs.append(idxs_l[i])
                    vals = res
                    idxs_l = idxs
                else:
                    res = []
                    idxs = []
                    for i, item in enumerate(vals):
                        if item <= args.get("lte"):
                            res.append(item)
                            idxs.append(idxs_l[i])
                    vals = res
                    idxs_l = idxs
        if args.get("eq") != None:
            res = []
            idxs = []
            for i, item in enumerate(vals):
                if item == args.get("eq"):
                    res.append(item)
                    idxs.append(idxs_l[i])
            vals = res
            idxs_l = idxs
        return Time(values= vals,
                    name= doc["name"],
                    units= doc["units"],
                    dimensions=doc["dimensions"],
                    indexes=idxs_l)

    def resolve_human(self, info, name=None):
        print("call {0}".format(name))
        return None

    def resolve_pres(self, info, **args):
        print(args)
        client = pymongo.MongoClient(mongoURI)
        db = client[args.get('dataSet')]
        coll = db["PRES"]

        f = {}
        s = {}
        doc = coll.find_one()
        vals = doc["values"]
        if args.get("time") != None:
            res = []
            result = schema.execute(args.get("time"))
            for val in result.data["time"]["indexes"]:
                res.append(doc["values"][val])
            vals = res
        return Pres(values=vals,
                    name=doc["name"],
                    units=doc["units"],
                    dimensions=doc["dimensions"])


schema = graphene.Schema(query=Query)