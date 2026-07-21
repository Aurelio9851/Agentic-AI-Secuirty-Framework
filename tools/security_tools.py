import os


SECURITY_PATTERNS = [

    "password=",

    "secret=",

    "api_key",

    "eval(",

    "exec(",

    "SELECT * FROM"

]



def security_scan(path="."):


    findings=[]


    for root, dirs, files in os.walk(path):

        for file in files:

            filepath=os.path.join(
                root,
                file
            )


            try:

                content=open(
                    filepath,
                    errors="ignore"
                ).read()


                for pattern in SECURITY_PATTERNS:

                    if pattern.lower() in content.lower():

                        findings.append({

                            "file": filepath,

                            "pattern": pattern

                        })


            except:

                pass


    return findings