import sys

import LabWAS


if __name__ == "__main__":
    study_type = sys.argv[1]
    if study_type == 'labwas':
        LabWAS.run()
    