from src.aple.core.session import ApleSession
from src.aple.ui.console import ConsoleUI
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    ui = ConsoleUI()
    ui.display_header()
    
    try:
        topic = ui.get_topic()
        
        session = ApleSession(topic, ui)
        session.run()

        ui.display_summary(session.assessment_results)
        ui.display_report(session.evaluation_report)

    except Exception as e:
        ui.display_error(f"A critical error occurred: {e}")
    finally:
        ui.display_footer()

if __name__ == "__main__":
    main()