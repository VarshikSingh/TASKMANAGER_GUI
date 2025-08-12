import json
import tkinter as tk
from tkinter.font import BOLD

class TM():
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task_name):
            self.tasks.append({'task' : task_name, 'completed' : False})
            self.save_tasks()
    
    def delete_task(self, task_name):
        for index,task in enumerate(self.tasks):
            if task['task'] == task_name:
                self.tasks.pop(index)
                self.save_tasks()
                break 

    def mark_complete(self, task_name):        
        for task in self.tasks:
            if task['task'] == task_name:
                task['completed'] = True 
        self.save_tasks()
 
    def save_tasks(self):
        with open('tasks.json', 'w') as f :
            json.dump(self.tasks, f)
    
    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f :
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            self.tasks = []


class ToDoGUI():
    def __init__(self, root , Task_manager):
        
        self.root = root
        self.tm = Task_manager 
        self.drag_index = None
        self.click_index = None

        self.heading = tk.Label(self.root, text="🗂️ My ToDo List", font=("Helvetica", 16, "bold"))
        self.heading.grid(row=0, column=4, padx=10, pady=10)

        self.menu = tk.Menu(root)
        self.menu.add_command(label = 'delete', command = lambda: self.UI_del(self.click_index))
        self.menu.add_command(label = 'mark complete', command = lambda: self.UI_mc(self.click_index))
        self.menu.add_separator()
        self.menu.add_command(label = 'exit', command = self.exit)
        

        self.add_label = tk.Label(root, text = 'ADD TASK : ')
        self.add_label.grid(row = 1, column = 0)       
        self.entry = tk.Entry(root,width = 30)
        self.entry.grid(row=1, column=1)
        self.entry.bind("<Return>", lambda event: self.add())

        self.del_label = tk.Label(root, text = 'DELETE TASK : ')
        self.del_label.grid(row = 2, column = 0) 
        self.entry2 = tk.Entry(root, width =30)
        self.entry2.grid(row = 2, column = 1)      
        self.entry2.bind("<Return>", lambda event:  self.delete())
        
        self.mark_label = tk.Label(root, text = 'MARK COMPLETE : ')
        self.mark_label.grid(row = 3, column = 0) 
        self.entry3 = tk.Entry(root, width =30)
        self.entry3.grid(row = 3, column = 1)
        self.entry3.bind("<Return>", lambda event:  self.mc())
       
        self.tasks_list = tk.Listbox(root, height = 30, width = 100)
        self.tasks_list.grid(row =5, column =5)     
        self.tasks_list.bind("<ButtonPress-1>", self.on_click )
        self.tasks_list.bind("<B1-Motion>", self.on_drag)   
        self.tasks_list.bind("<ButtonRelease-1>", self.on_drop)  
        self.tasks_list.bind("<Button-3>", self.on_rclick)
        
        self.save_button = tk.Button(self.root, text = 'EXIT AND SAVE', command = self.exit, padx = 100, pady = 30 )
        self.save_button.grid(row=5, column=0)

        self.tm.load_tasks()
        self.refresh_list()

        

    def on_click(self, event):
        self.drag_index = self.tasks_list.nearest(event.y)
        index = self.click_index
    
    def on_rclick(self, event):
        self.click_index = self.tasks_list.nearest(event.y)
        self.menu.tk_popup(event.x_root, event.y_root)
        

    def on_drag(self, event):
        new_index = self.tasks_list.nearest(event.y)
        if new_index != self.drag_index:
            item = self.tasks_list.get(self.drag_index)
            self.tasks_list.delete(self.drag_index)
            self.tasks_list.insert(new_index, item)
            self.drag_index = new_index  

    def on_drop(self, event):
        self.drag_index = None

    def UI_del(self, index ):
        self.tm.tasks.pop(index)
        self.refresh_list()
        self.tm.save_tasks()
        
    def add(self):
        task_name = self.entry.get().strip()
        self.tm.add_task(task_name)
        self.entry.delete(0, tk.END)
        self.refresh_list()
        self.tm.save_tasks()
    
    def delete(self):
        task_name = self.entry2.get().strip()
        self.tm.delete_task(task_name)
        self.entry2.delete(0, tk.END)
        self.refresh_list()
        self.tm.save_tasks()
    
    def mc(self):
        task_name = self.entry3.get().strip()
        self.tm.mark_complete(task_name)
        self.entry3.delete(0, tk.END)
        self.refresh_list()
        self.tm.save_tasks()    

    def UI_mc(self, index):
        self.tm.tasks[index]['completed'] = True
        self.refresh_list()
        self.tm.save_tasks()
              
    def refresh_list(self):
        self.tasks_list.delete(0, tk.END)
        for task in self.tm.tasks:
            status = '✅' if task['completed'] else '❌'
            self.tasks_list.insert(tk.END, f"{task['task']} - {status}")
    
    def exit(self):
        self.tm.save_tasks()
        self.root.destroy()

            


    

    

root = tk.Tk()
Tm = TM()
app = ToDoGUI(root, Tm)
root.mainloop()
    