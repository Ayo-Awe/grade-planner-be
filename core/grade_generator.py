

FIVE_POINT_GP_SYSTEM = "5.0"
FOUR_POINT_GP_SYSTEM = "4.0"

four_point_grades_map = {
    4: "A",
    3: "B",
    2: "C",
    1: "D",
    # 0: "F"
}

five_point_grades_map = {
    5: "A",
    4: "B",
    3: "C",
    2: "D",
    # 0: "F"
}

MAX_COMBINATION = 10

# todo: Refactor grade generator


class GradeGenerator:
    def __init__(self, courses: list[dict], gp_system: str) -> None:
        self.credit_courses = list(filter(lambda c: c["unit"] > 0, courses))
        self.zero_credit_courses = list(
            filter(lambda c: c["unit"] == 0, courses))

        self.credit_units = list(map(lambda c: c["unit"], self.credit_courses))

        if gp_system == FOUR_POINT_GP_SYSTEM:
            self.grades_map = four_point_grades_map
        else:
            self.grades_map = five_point_grades_map

    def generate(self, target_grade_point_sum: int):
        grade_combos = self.__find_grade_combinations(target_grade_point_sum)

        grouped_result_sets = self.__group_result_sets(grade_combos)

        patterns = []

        for g in grouped_result_sets:
            g["generated_grades"] = g["combos"][0]
            g.pop("combos")
            patterns.append(g)

        return patterns

    def __find_grade_combinations(self, target_grade_point_sum) -> list[list[int]]:
        all_possible_course_grades = []

        for course in self.credit_courses:
            possible_course_grades = self.__get_possible_course_grades(course)
            all_possible_course_grades.append(possible_course_grades)

        memo = {}
        max_min_grade = [0]

        def backtrack(index, current_sum, current_combination):

            if (index, current_sum) in memo:
                return memo[(index, current_sum)]

            if index == len(all_possible_course_grades):
                if current_sum == target_grade_point_sum:
                    if self.__min_grade_in_result_set(current_combination) > max_min_grade[0]:
                        max_min_grade[0] = self.__min_grade_in_result_set(
                            current_combination)
                    return [list(current_combination)]
                return []

            if current_sum > target_grade_point_sum:
                return []

            if len(current_combination) > 0 and self.__min_grade_in_result_set(current_combination) < max_min_grade[0]:
                return []

            result = []

            # Try each value of the current unit
            for possible_grade in all_possible_course_grades[index]:
                # Update the current sum and combination
                grade_point = possible_grade["grade_int"] * \
                    possible_grade["unit"]

                new_sum = current_sum + grade_point
                new_combination = current_combination + [possible_grade]

                # Recursively explore the next unit
                result += backtrack(index + 1, new_sum,
                                    new_combination)

                # Backtrack: Reset the current sum and remove the last added value

            memo[(index, current_sum)] = result
            return result

        return backtrack(0, 0, [])

    def __get_possible_course_grades(self, course):
        possible_grades = []

        for grade_int, grade in self.grades_map.items():
            possible_grade = {**course, "grade_int": grade_int, "grade": grade}
            possible_grades.append(possible_grade)

        return possible_grades

    def __min_grade_in_result_set(self, result_set: list[dict]):
        min_grade = 100000

        for course in result_set:
            if course["grade_int"] < min_grade:
                min_grade = course["grade_int"]

        return min_grade

    def __group_result_sets(self, result_sets):

        r_sets = self.__dedupe_result_sets(result_sets)

        solns = []

        for rs in r_sets:
            pattern = {}

            for course in rs:
                unit = course["unit"]
                grade = course["grade"]

                if pattern.get(unit) == None:
                    pattern[unit] = {}

                if pattern.get(unit).get(grade) == None:
                    pattern[unit][grade] = 0

                pattern[unit][grade] += 1

            index = next((i for i, soln in enumerate(
                solns) if soln["pattern"] == pattern), None)

            if index is None:
                soln = {"pattern": pattern, "combos": []}
                solns.append(soln)
                index = len(solns)-1

            if len(solns[index]["combos"]) < 10:
                solns[index]["combos"].append(rs)

        for i, _ in enumerate(solns):
            soln = solns[i]

            def add_grades(course: dict) -> dict:
                course["grade"] = "A"
                course["grade_int"] = 5
                return course

            zero_credit_courses = [add_grades(course)
                                   for course in self.zero_credit_courses]

            soln["pattern"]["0"] = {
                "A": len(zero_credit_courses)
            }

            for j, _ in enumerate(soln["combos"]):
                combo = soln["combos"][j]
                combo.extend(zero_credit_courses)

        return solns

    def __dedupe_result_sets(self, result_sets):
        # for each result set, create a tuple of grades
        # zip the courses with the result sets and add the grades
        tups = [tuple([course["grade_int"]
                       for course in result_set]) for result_set in result_sets]

        res_set = set(tups)

        unique_result_set = []

        for res in res_set:
            result_set = []
            for grade, course in zip(res, self.credit_courses):
                c = course.copy()
                c["grade_int"] = grade
                c["grade"] = self.grades_map[grade]
                result_set.append(c)
            unique_result_set.append(result_set)

        return unique_result_set
