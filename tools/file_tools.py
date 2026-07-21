import os


def list_files(path="."):

    result=[]

    for root, dirs, files in os.walk(path):

        for f in files:
            result.append(
                os.path.join(root,f)
            )

    return result[:100]



def grep_file(keyword):

    matches=[]

    for root, dirs, files in os.walk("."):

        for f in files:

            try:

                path=os.path.join(root,f)

                text=open(
                    path,
                    errors="ignore"
                ).read()

                if keyword.lower() in text.lower():
                    matches.append(path)

            except:
                pass


    return matches