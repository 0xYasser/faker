from faker import Faker
import sys, os, random, json,csv


class FakerSchema():

    def __init__(self, obj, preserve_seed = False, form = None):
        self.json_object = json.loads(obj)
        self.preserve_seed = preserve_seed
        self.filename = self._get_scheam_attr('filename')
        self.form = self._get_scheam_attr('form') if not form else form
        self.elements = self._get_scheam_attr('elements')

        try:
            self.seed = self.json_object['seed']
        except:
            self.seed = random.randrange(sys.maxsize)
        
        self.fake = Faker()
        self.fake.seed(self.seed)

    def _get_scheam_attr(self, attr):
        if self.json_object:
            try:
                return self.json_object[attr]
            except:
                raise NotImplementedError("\'"+attr + "\' does not exist")

    def _get_element_attr(self, element, key):
        if self.elements:
            for elm in self.elements:
                if elm == element:
                    try:
                        return self.elements[element][key]
                    except:
                        raise ValueError("\'"+element+"\' does not have "+key)
            raise NotImplementedError("\'"+element + "\' does not exist")

    def _get_accepeted_types(self):
        if self.form == 'obj' or self.form == 'object':
            _accepted_types = (object)
        else:
            _accepted_types = (int, float, str, bool, dict, list, tuple)

        return _accepted_types

    def _return_json(self, data):
        with open(self.filename+'.json', 'w') as outfile:
            json.dump(data, outfile)

    def _return_csv(self, data):
        with open(self.filename+'.csv', 'w') as outfile:
            w = csv.writer(outfile)
            w.writerows([data.keys()])
            w.writerows(data.values())

    def _return_type(self, form:str, data):
        if form.lower() == "json":
            self._return_json(data)
        if form.lower() == "csv":
            self._return_csv(data)
        if form.lower() == "obj" or self.form == 'object':
            return data
            
    def generate(self,num_of_rows=1):
        data = {}
        if self.preserve_seed:
            data['seed'] = self.seed
        for elm in self.elements:
            generator = self._get_element_attr(elm, 'generator')
            try:
                parameters = self._get_element_attr(elm, 'parameters')
            except:
                parameters = None
            func = getattr(self.fake, generator)

            data[elm] = self._generate_values(func, parameters, num_of_rows)
        return self._return_type(self.form, data)

    def _generate_values(self,func, param, num_of_rows:int):
        data = []
        for _ in range(num_of_rows):
            value = func(**param) if param else func()
            if not isinstance(value, self._get_accepeted_types()):
                value = str(value)
            data.append(value)
        
        return data if len(data) > 1 else data[0]


class JsonSchema():
    pass


if __name__ == "__main__":
    obj = """
    {
        "filename": "Person",
        "seed":7195481086956804997,
        "form":"csv",
        "elements": {
            "elem1": {
                "generator":"name",
                "description":""
            },
            "elem2": {
                "generator":"address",
                "description":""
            },
            "elem3": {
                "generator":"color_name",
                "description":""
            },

            "elem4": {
                "generator":"date_between",
                "description":"blah",
                "parameters": {"start_date": "-1y", "end_date": "today"}
            }
        }
    }
    """
    o = FakerSchema(obj)
    o.generate(3)


