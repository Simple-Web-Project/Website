import json
import os
import logging


generic_header = """
<!DOCTYPE html>
<html lang="en">

<head>
    <title>Simple Web</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {
    background-color: #FFFFFF;
    color: #292529;
    max-width: 800px;
    margin: 10px auto;
    padding: 10px;
}

img {
    padding: 5px;
    width: 250px;
}

table {
    width: 100%;
    margin: 25px 0;
    padding: 12px 15px;
    border: 1px solid;
    border-collapse: collapse;
}

table td, table th {
    border: 1px solid;
}

@media screen and (prefers-color-scheme: dark) {
    body {
        background-color: #101316;
        color: #ccc;
    }

    a:visited {
        color: #9759f6;
        text-decoration: none;
    }

    a {
        color: #599bf6;
        text-decoration: none;
    }
}

</style>
</head>

<body>
"""

index_style = """
<style>
.no-margin {
    margin: 0;
}

section {
    background-color: #eee;
    color: #292529;
    margin: 1rem auto;
    padding: 1rem;
}

@media screen and (prefers-color-scheme: dark) {
    section {
        background-color: #16191c;
        color: #ccc;
    }
}

</style>
"""

generic_ending = """
</body>
</html>
"""



def load_config() -> dict:
    config_file = open("config.json")
    config = json.load(config_file)
    config_file.close()
    logging.info("Read config file")
    return config

def generate_index(config: dict):
    with open("index.html", "w") as index:
        index.write(generic_header)
        index.write(index_style)

        index.write("<h1>The Simple Web Project</h1>")
        index.write("<p>" + config["description"] + "</p>")


        index.write("<h2>Projects</h2>")

        for project in config["projects"]:
            project_id = project["id"]
            project_name = project.get("name") or "Unnamed Project"
            project_short_description = project.get("short_description") or ""


            project_notice = project.get("notice") or ""


            index.write(f"""
            <section>
                <h3 class="no-margin">
                    <a href=\"projects/{project_id}.html\">{project_name}</a> <a style=\"color: red\">{project_notice}</a>
                </h3><p>
            """)

            ## BUILD INSTANCE DESCRIPTION BAR ##

            instance_desc_bar = ""
            for itype in config["instance_types"]:
                count = len(project.get(itype["list_name"]) or [])
                if count == 0:
                    continue

                display_name = itype["name"] + " Instances"
                icon = itype["icon"]

                if len(instance_desc_bar) > 0:
                    instance_desc_bar += " • "
                instance_desc_bar += f"<span title=\"{count} {display_name}\">{icon} <strong>{count}</strong></span>"

            if len(instance_desc_bar) == 0:
                index.write("No Instances")
            else:
                index.write(instance_desc_bar)

                #<p><span title=\"{instance_count} Instances\">🌐 <strong>{instance_count}</strong></span> • <span title=\"{onion_instance_count} Onion Instances\">🧅 <strong>{onion_instance_count}</strong></span> • <span title=\"{i2p_instance_count} I2P Instances\">⬤ <strong>{i2p_instance_count}</strong></span> • <span title=\"{loki_instance_count} Lokinet Instances\">⧖ <strong>{loki_instance_count}</strong></span></p>
            index.write(f"""</p>
                <blockquote class="no-margin">
                <p class="no-margin">{project_short_description}</p>
                </blockquote>
            </section>
            """)

        if len(config["other_frontends"]) > 0:
            index.write("""
                <h2>Other Frontends</h2>
                <p>These are some other frontends that we would like to promote, these are <span style="color: red">NOT part of the Simple Web Project</span></p>
                <p>Also check out the Libredirect Browser Extension: <a href="https://libredirect.github.io">LibRedirect</a></p>
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Frontend For</th>
                        <th>Source Code</th>
                    </tr>
            """)

            for other_frontend in config["other_frontends"]:
                frontend_name = other_frontend["name"]
                frontend_for_name = other_frontend["frontend_for"]["name"]
                frontend_for_link = other_frontend["frontend_for"]["link"]
                frontend_source = other_frontend["source_code"]
                frontend_website = other_frontend["website"]

                source_forge = "Source Code"
                if frontend_source.startswith("https://sr.ht") or frontend_source.startswith("https://git.sr.ht"):
                    source_forge = "Sourcehut"
                elif frontend_source.startswith("https://github.com"):
                    source_forge = "Github"
                elif frontend_source.startswith("https://gitlab.com"):
                    source_forge = "Gitlab"
                elif frontend_source.startswith("https://codeberg.org"):
                    source_forge = "Codeberg"

                index.write(f"""
                    <tr>
                        <td><a href="{frontend_website}">{frontend_name}</a></td>
                        <td><a href="{frontend_for_link}">{frontend_for_name}</a></td>
                        <td><a href="{frontend_source}">{source_forge}</a></td>
                    </tr>
                """)

            index.write("</table>")

        matrix_homeserver = config["contact"]["matrix"]["homeserver"]
        matrix_room = config["contact"]["matrix"]["room"]
        irc_channel = config["contact"]["irc"]
        email_address = config["contact"]["email"]

        index.write("<h2>Contact</h2>")
        index.write(f"<strong>IRC:</strong> {irc_channel} <br>")
        index.write(f"<strong>Matrix:</strong> <a href=\"https://matrix.to/#/{matrix_room}:{matrix_homeserver}\">{matrix_room}:{matrix_homeserver}</a> <br>")
        index.write(f"<strong>Email:</strong> <a href=\"mailto:{email_address}\">{email_address}</a>")

        index.write(generic_ending)

def generate_projects(config: dict):
    if not os.path.exists("projects"):
        os.mkdir("projects")
    for project in config["projects"]:
        id_ = project["id"]
        name = project.get("name") or "Unnamed Project"
        description = project.get("description") or ""
        screenshots = project.get("screenshots") or []
        main_contributors = project.get("main_contributors") or []

        official_tools = project.get("official_tools") or []
        unofficial_tools = project.get("unofficial_tools") or []
        shoutouts = project.get("shoutouts") or []

        notice = project.get("notice") or ""

        with open(f"projects/{id_}.html", "w") as f:
            f.write(generic_header)
            f.write(f"""
            <h1>{name}</h1>\n
            <hr>\n
            <p>{description}</p>\n
            """)
            # Screenshots
            if len(screenshots) > 0:
                f.write("<h2>Screenshots</h2>")
                for screenshot in screenshots:
                    scr_src = screenshot["src"]
                    scr_desc = screenshot["description"]
                    f.write(f"<a href=\"../screenshots/{scr_src}\" target=\"_blank\">")
                    f.write(f"<img src=\"../screenshots/{scr_src}\" alt=\"{scr_desc}\">")
                    f.write("</a>")
                f.write("<br>")

            # Main Contributors
            if len(main_contributors) > 0:
                f.write("<h2>Main Contributors</h2>")
                for contributor in main_contributors:
                    c_name = contributor["name"]
                    c_link = contributor.get("link")

                    if c_link != None:
                        f.write(f"<li><a href=\"{c_link}\">{c_name}</a></li>")
                    else:
                        f.write(f"<li>{c_name}</li>")
                f.write("<br>")
            
            for itype in config["instance_types"]:
                instances = project.get(itype["list_name"]) or []
                count = len(instances)
                icon = itype["icon"]
                iid = itype["id"]
                name = itype["name"] + " Instances"
                protocol = itype["protocol"]

                if count > 0:
                    f.write(f"<h2>{icon} {name} ({count})</h2>")
                    f.write(f"<p>If you want to use this list of instances in your project, just refer to <a href=\"https://simple-web.org/instances/{id_}{iid}\">https://simple-web.org/instances/{id_}{iid}</a></p>")

                    f.write("<ul>")
                    for instance in instances:
                        f.write(f"<li><a href=\"{protocol}://{instance}\">{instance}</a></li>")
                    f.write("</ul>")

            f.write("<h3>Want your instance to be added to the list?</h2>")
            f.write("<p>You can refer to the <a href=\"https://codeberg.org/SimpleWeb/Website/src/branch/master/README.md\">README.md</a> of this Website for more information.</p>")

            if (len(official_tools) > 0 or
               len(unofficial_tools) > 0 or
               len(shoutouts) > 0):
                   f.write("<hr>")

            # Official Tools
            if len(official_tools) > 0:
                f.write("<h2>Official Tools/Clients</h2>")
                f.write("<ul>")
                for tools in official_tools:
                    link = tools["link"]
                    name = tools["name"]
                    f.write(f"<li><a href=\"{link}\">{name}</a></li>")
                f.write("</ul>")

            # Unofficial Tools
            if len(unofficial_tools) > 0:
                f.write("<h2>Unofficial Tools/Clients</h2>")
                f.write("<ul>")
                for tools in unofficial_tools:
                    link = tools["link"]
                    name = tools["name"]
                    f.write(f"<li><a href=\"{link}\">{name}</a></li>")
                f.write("</ul>")

            # Shoutouts
            if len(shoutouts) > 0:
                f.write("<h2>Shoutouts</h2>")
                f.write("<p>These are some other projects that we like</p>")
                f.write("<ul>")
                for tools in shoutouts:
                    link = tools["link"]
                    name = tools["name"]
                    f.write(f"<li><a href=\"{link}\">{name}</a></li>")
                f.write("</ul>")

            f.write("<hr>")
                
            source_code = project["source_code"]

            f.write(f"<a href=\"../index.html\">Go Back</a> | <a href=\"{source_code}\">Source Code</a>")
            f.write(generic_ending)

def generate_instances(config: dict):
    if not os.path.exists("instances"):
        os.mkdir("instances")

    for project in config["projects"]:
        id_ = project["id"]
        name = project.get("name") or "Unnamed Project"

        for itype in config["instance_types"]:
            instances = project.get(itype["list_name"]) or []
            count = len(instances)
            display_name = itype["name"] + " Instances"
            iid = itype["id"]

            if count > 0:
                with open(f"instances/{id_}{iid}", "w") as f:
                    for instance in instances:
                        f.write(f"{instance}\n")

if __name__ == "__main__":
    config = load_config()
    generate_index(config)
    generate_projects(config)
    generate_instances(config)
