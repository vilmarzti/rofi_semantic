import re
import subprocess

from xdg.DesktopEntry import DesktopEntry


class Entry(DesktopEntry):
    """Entry.
    """

    def __init__(self, path):
        """__init__.

        Args:
            path:
        """
        super.__init__(self, path)

        self.name = self.getName()
        self.icon = self.getIcon()
        self.exec = self.getExec()
        self.desc = self.getDescription()

    def __repr__(self):
        return f"{self.name};{self.icon};{self.exec};{self.desc}"

    def set_embedding(self, embedding):
        """Set Embedding gotten from latent space

        Args:
            embedding: Array of Numbers
        """
        self.embedding = embedding

    def get_whatis_entry(self):
        """ Use 'whatis <command>' to get a natural language description.

            Returns:
                Whatis description of xdg entry or None if
                command is not found.
        """
        name = self.getName()
        command = re.match(r'\S*', self.getExec())

        if command is None:
            return None

        whatis_cmd = subprocess.run(
                ['whatis', '-l', command],
                capture_output=True
                )

        description = None
        if whatis_cmd.returncode == 0:
            description = re.sub(
                    r'^.*-', f'{name}:', whatis_cmd.stdout.decode('utf-8')
                    )
            description = re.sub(r'(\n.*)*', '', description)

        return description

    def get_description(self):
        """Check 'whatis' or xdg entry comment for natural language description

        Args:
            xdg_entry: Parsed xdg entry

        Returns:
            Natural Lanugange descrption of xdg entry
        """

        description = self.get_whatis_entry()

        if description is None and (comment := self.getComment()) != '':
            description = f'{self.name}: {comment}'

        if description is None:
            description = f'{self.name}'

        return description
