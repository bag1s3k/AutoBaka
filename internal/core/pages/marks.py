class MarksPage(BasePage):
    """
    Inherits from BasePage
    Use for get marks
    """
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.SUBJECTS = {}

    @validate_output(
        error_msg="Getting marks failed",
        success_msg="Getting marks successful",
        level="critical"
    )
    def get_marks(self) -> dict[str, list[dict[str, str]]]:
        """
        Specific logic to get marks
        :return: empty dict if fail otherwise filled dict
        """
        try:
            logger.info("Looking for an element on page with marks")

            marks_line = self._find_items(target=(By.XPATH,
                                                        "//tbody//tr[//td "
                                                        "and contains(@class, 'dx-row') "
                                                        "and contains(@class, 'dx-data-row') "
                                                        "and contains(@class, 'dx-row-lines')]"))

            # Load whole marks (date, mark, value...) it's line of these data
            if not marks_line:
                logger.error(f"Marks not found url: {self.driver.current_url} title: {self.driver.title}")
                self.SUBJECTS = {}
                return self.SUBJECTS

            for single_line in marks_line:
                subject = self._find_items(target=(By.TAG_NAME, "td"), parent=single_line)

                if not subject:
                    logger.warning("No subject")
                    self.SUBJECTS = {}
                    return self.SUBJECTS

                mark = subject[1].text
                topic = unidecode(subject[2].text)
                weight = subject[5].text
                date = subject[6].text
                subject_name = unidecode(subject[0].text)

                logger.info(f"Extracting: {mark} {topic} {weight} {date} {subject_name}")

                self.SUBJECTS.setdefault(subject_name, []).append({
                    "mark": mark,
                    "topic": topic,
                    "weight": weight,
                    "date": date
                })

            # Export marks to json file
            export_json(self.SUBJECTS, RAW_MARKS_OUTPUT)

            return self.SUBJECTS

        except Exception as e:
            logger.exception(e)
            self.SUBJECTS = {}
            return self.SUBJECTS

    @validate_output(
        error_msg="Processing marks failed or there are no marks",
        success_msg="Processing marks successful",
        level="error"
    )
    def process_marks(self) -> bool:
        """
        Specific logit to process marks

        :return subjects: sorted dict of processed marks
        """

        if not self.SUBJECTS: return False

        logger.info(f"Processing marks")

        # (1- -> 1.5) or N don't add to the list and Calculate average
        text_to_num = [4.5, 3.5, 2.5, 1.5]
        for subject, list_subject in self.SUBJECTS.items():
            logger.info(f"Processing subject: {subject}")
            try:
                marks = []
                for dict_mark in list_subject:
                    if "-" in dict_mark["mark"]:
                        dict_mark["mark"] = text_to_num[-int(dict_mark["mark"][
                                                                 0])]  # take 1. char of '2-' => 2 and 2 * (-1) => -2 is index of a list (text_to_num)
                    elif dict_mark["mark"].isdigit():
                        dict_mark["mark"] = int(dict_mark["mark"])
                    else:
                        continue

                    marks.append([dict_mark["mark"], dict_mark["weight"]])

                # Calculate averages
                logger.info("Calculating average")

                mark_times_weight = 0
                weight_sum = 0

                for mark in marks:
                    mark_times_weight += float(mark[0]) * float(mark[1])
                    weight_sum += float(mark[1])

                average = 0
                if weight_sum != 0:
                    average = round(mark_times_weight / weight_sum, 2)
                else:
                    logger.warning(f"{subject} has no weight")

                self.SUBJECTS[subject].append({"avg": average})

                # Export marks to json file
                export_json(self.SUBJECTS, MARKS_OUTPUT)

            except Exception as e:
                logger.exception(f"Something happened during processing marks: {e}")
                return False

        self.SUBJECTS = dict(sorted(self.SUBJECTS.items()))
        export_results(self.SUBJECTS, config.get_auto_cast("PATHS", "result_path"))

        return True