from abc import abstractmethod, ABC


class ClassInfo(ABC):
    @abstractmethod
    def terminal_show(self, book):
        pass


class AllContactInfo(ClassInfo):
    def terminal_show(self, book):
        if len(book) == 0:
            return f"Your contacts list is empty"
        line = ""
        for record in book.values():
            line += f"{record}\r"
        return line
    
    def terminal_print_show(self, book):
        result = self.terminal_show(book)
        print(result)


class ContactInfo(ClassInfo):
    def terminal_show(self, book, *args):
        if len(book) == 0:
            return f"Your contacts list is empty"
        stop = int(args[0])
        line = ""
        for rec in book.iterator(stop):
            line += rec
        return line
    
    def terminal_print_show(self, book, *args):
        result = self.terminal_show(book, *args)
        print(result)


class AllNoteInfo(ClassInfo):
    def terminal_show(self, note):
        return note
    
    def terminal_print_show(self, note):
        result = self.terminal_show(note)
        print(result)
    

class NoteSearch(ClassInfo):
    def terminal_show(self, note, *args):
        keyword = " ".join(args)
        if not keyword:
            raise ClassInfo
        return note.search_notes(keyword)
    
    def terminal_print_show(self, note, *args):
        result = self.terminal_show(note, *args)
        print(result)