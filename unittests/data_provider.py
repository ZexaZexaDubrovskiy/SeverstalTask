class DataProvider:
    @staticmethod
    def rolls():
        return [
            {"id": 1, "weight": 200, "lenght": 200},
            {"id": 1, "weight": 200, "lenght": 200},
            {"id": 1, "weight": 200, "lenght": 200},
        ]

#todo сделать через циклы
    @staticmethod
    def storage():
        return [
            {"id": 1, "roll_id": 4},
            {"id": 2, "roll_id": 3},
            {"id": 3, "roll_id": 2},
            {"id": 4, "roll_id": 6},
            {"id": 5, "roll_id": 8},
            {"id": 6, "roll_id": 9},
        ]
