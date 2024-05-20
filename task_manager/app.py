import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine('sqlite:///task_manager.db')
Session = sessionmaker(bind=engine)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    due_date = Column(Date)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(engine)

def add_task(title, description, priority, due_date):
    session = Session()
    task = Task(
        title=title, 
        description=description, 
        priority=priority, 
        due_date=due_date,
        completed=False
    )
    session.add(task)
    session.commit()
    session.close()

def get_tasks():
    session = Session()
    tasks = session.query(Task).all()
    session.close()
    return tasks

def update_task_status(task_id, completed):
    session = Session()
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        task.completed = completed
        session.commit()
    session.close()

def delete_task(task_id):
    session = Session()
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        session.delete(task)
        session.commit()
    session.close()

def main():
    st.title("📋 Task Management App")
    
    # Sidebar for adding tasks
    st.sidebar.header("Add New Task")
    title = st.sidebar.text_input("Task Title")
    description = st.sidebar.text_area("Task Description")
    priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"])
    due_date = st.sidebar.date_input("Due Date", datetime.date.today())
    
    if st.sidebar.button("Add Task"):
        add_task(title, description, priority, due_date)
        st.sidebar.success("Task added successfully!")
    
    # Main area with tabs
    tab1, tab2, tab3 = st.tabs(["Task List", "Task Analytics", "Completed Tasks"])
    
    with tab1:
        st.header("Current Tasks")
        tasks = get_tasks()
        
        for task in tasks:
            if not task.completed:
                with st.expander(f"{task.title} - {task.priority} Priority"):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**Description:** {task.description}")
                        st.write(f"**Due Date:** {task.due_date}")
                    
                    with col2:
                        if st.button(f"Complete {task.id}", key=f"complete_{task.id}"):
                            update_task_status(task.id, True)
                            st.experimental_rerun()
                    
                    with col3:
                        if st.button(f"Delete {task.id}", key=f"delete_{task.id}"):
                            delete_task(task.id)
                            st.experimental_rerun()
    
    with tab2:
        st.header("Task Analytics")
        if tasks:
            # Priority Distribution
            priority_counts = {}
            for task in tasks:
                priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
            
            fig1 = px.pie(
                values=list(priority_counts.values()), 
                names=list(priority_counts.keys()), 
                title='Task Priority Distribution'
            )
            st.plotly_chart(fig1)
            
            # Tasks by Month
            task_months = [task.due_date.strftime("%B") for task in tasks]
            month_counts = {}
            for month in task_months:
                month_counts[month] = month_counts.get(month, 0) + 1
            
            fig2 = go.Figure(data=[
                go.Bar(x=list(month_counts.keys()), y=list(month_counts.values()))
            ])
            fig2.update_layout(title='Tasks by Month', xaxis_title='Month', yaxis_title='Number of Tasks')
            st.plotly_chart(fig2)
    
    with tab3:
        st.header("Completed Tasks")
        completed_tasks = [task for task in tasks if task.completed]
        
        for task in completed_tasks:
            with st.expander(f"{task.title} - Completed"):
                st.write(f"**Description:** {task.description}")
                st.write(f"**Completed On:** {datetime.date.today()}")

if __name__ == "__main__":
    main()
