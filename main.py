# -*- coding: utf-8 -*-

from schema import schema as s

if __name__ == '__main__':
    # print('schema is {0}'.format(s))
    query1 = """
        query {
          time(dataSet:"MO_201708_PR_PF_6903279",lt:24705.21747685185) {
            values
            indexes}}
    """

    query2 = """
            query getPres($time: String){
              pres(dataSet:"MO_201708_PR_PF_6903279",time:$time,) {
                name
                values}}
        """
    result = s.execute(query2, variables={"time":query1})
    print(result.data)
    print(result.errors)

q = """
    SELECT $pres = query {
    pres(dataSet:"MO_201708_PR_PF_6903279", time:$time) {
                name
                values
                units
              }
    }
    WHERE $time = query {
          time(dataSet:"MO_201708_PR_PF_6903279",eq:24705.21747685185) {
            values
            indexes
          }
"""

def process(query):


    return