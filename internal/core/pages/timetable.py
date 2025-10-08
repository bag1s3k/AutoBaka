class Timetable(BasePage):
    """
    Inherits BasePage
    Use for get timetable (in code is used shortcut TT or tt for timetable)
    """

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.NORMAL_TT_DAYS = "//div[@class='day-row normal']"
        self.NORMAL_TT_DATES = ".//div/div/div/div/span"
        self.NORMAL_TT_LECTURES = (".//div/div/span/div/div[@class='empty']"
                                   " | .//div/div/span/div/div/div[@class='top clearfix']"
                                   " | .//div/div/span/div/div/div/div[2]")
        self.NEXT_TT_BTN = '//*[@id="cphmain_linkpristi"]'
        self.PERMANENT_TT_BTN = '//*[@id="cphmain_linkpevny"]'
        self.PERMANENT_TT_DAYS = "//div[@class='day-row double']"

        self.SEMESTER_END = datetime.strptime(config.get_auto_cast("DATES", "semester1_end"), "%Y-%m-%d").date()
        self.timetable = {}

    @validate_output(
        error_msg="Extracting timetable failed",
        success_msg="Extracting timetable successful",
        level="error"
    )
    def _extract_tt(self, days_xpath, date_xpath=None, lectures_xpath=None, last_date=None, dual=False) -> dict:
        """
        Specific logic to get specific timetable
        :param days_xpath:
        :param date_xpath:
        :param lectures_xpath:
        :param last_date:
        :return: Empty dict if fail otherwise filled dict
        """
        try:
            days = self._find_items((By.XPATH, days_xpath))

            if n_days := len(days) != 5:
                logger.debug(f"Wrong amount of days: {n_days} there must be 5")

            n = 3  # TODO: FIX ME
            for day in days:
                year = datetime.now().year
                lectures = []

                # ------- SINGLE TT ------ #
                if not dual:
                    date_raw = self._find_item((By.XPATH, date_xpath), parent=day)
                    date_raw = datetime.strptime(f"{date_raw.text}/{year}", "%d/%m/%Y")
                    lectures_t = self._find_items((By.XPATH, lectures_xpath), parent=day)
                    lectures = [i.text for i in lectures_t]

                # ------- DUAL TT ------- #
                else:
                    new_last_date = datetime.strptime(str(f"{last_date}"), "%Y-%m-%d")
                    date_raw = new_last_date + timedelta(days=n)
                    n += 1  # TODO: FIX ME

                    double_lectures = self._find_items((By.XPATH, ".//div/div/span/div"), parent=day)

                    for single_lectures in double_lectures:
                        double_lecture = self._find_items(
                            (By.XPATH, ".//div[@class='empty'] | .//div/div/div[2]"),
                            parent=single_lectures)
                        lectures_to_string = [t.text for t in double_lecture]
                        for i, x in enumerate(lectures_to_string[:]):
                            if i % 2 == 0: lectures_to_string.remove(x)

                        lectures.append(lectures_to_string)

                if date_raw.weekday() in [6, 7]: continue  # skip Sat, Sun

                # Fill dict
                date = date_raw.date().isoformat()
                self.timetable[date] = []
                for lecture in lectures:
                    self.timetable[date].append(lecture)

                # One day of timetable should have 10 lessons
                if (n_timetable := len(self.timetable[date])) != 10:
                    logger.debug(f"Wrong amount of lectures: {n_timetable} there must be 10")

            export_json(self.timetable, TIMETABLE_OUTPUT)
            return self.timetable

        except Exception as e:
            logger.exception(f"Something unexcepted happened: {e}")
            return {}

    def get_tt(self):
        """
        It's help func, it calls other functions (extract_tt or find_item)
        :return: true if successful otherwise None
        """
        self._extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        self._find_item((By.XPATH, self.NEXT_TT_BTN)).click()
        self._extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        self._find_item((By.XPATH, self.PERMANENT_TT_BTN)).click()
        self._extract_tt(
            days_xpath=self.PERMANENT_TT_DAYS,
            last_date="2025-10-10",  # TODO: FIX ME
            dual=True
        )