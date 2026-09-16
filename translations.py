"""Static UI string translations (English, French, Arabic).

Only chrome text (titles, labels, buttons, captions, messages) lives here.
AI-generated recommendation text and Ask AI answers/questions are never
routed through this module — they stay in whatever language the user
typed or the model responded in.

Streamlit has no native RTL support, so Arabic text renders correctly but
the overall page layout direction does not flip. That is an accepted
limitation of this pass.
"""

LANGUAGE_NAMES = {
    "en": "English",
    "fr": "Français",
    "ar": "العربية",
}

EN = {
    # Shared
    "no_business_warning": "No business selected. Please go to the home page first.",
    "date_label": "Date",
    "notes_label": "Notes (optional)",
    "cost_label": "Cost",
    "currency_label": "Currency",
    "energy_source_label": "Energy Source",
    "units_kwh_label": "Units Consumed (kWh)",
    "diesel_liters_label": "Diesel Used (liters)",
    "hours_run_label": "Hours Run",
    "time_of_day_label": "Time of Day",
    "time_of_day_morning": "Morning",
    "time_of_day_afternoon": "Afternoon",
    "time_of_day_evening_night": "Evening/Night",
    "cancel_button": "Cancel",
    "total_outage_hours_metric": "Total Outage Hours",
    "source_grid": "Grid",
    "source_generator": "Generator",
    "source_solar": "Solar",

    # Sidebar navigation labels (used by st.Page(title=...) in app.py)
    "nav_home": "Home",
    "nav_log_entry": "Log Entry",
    "nav_dashboard": "Dashboard",
    "nav_ask_ai": "Ask AI",
    "nav_recommendations": "Recommendations",
    "nav_log_outage": "Log Outage",
    "nav_solar_payback": "Solar Payback",
    "nav_whatif": "What If Simulator",

    # app.py
    "app_title": "⚡ Energy Cost Tracker",
    "app_subtitle": "Track and understand your business's energy costs across grid, generator, and solar.",
    "active_business_label": "Active Business",
    "add_business_expander": "➕ Add a new business",
    "business_name_label": "Business name",
    "create_business_button": "Create Business",
    "enter_business_name_warning": "Please enter a business name.",
    "exchange_rate_expander": "💱 Exchange Rate Settings",
    "current_rate_text": "Current rate: 1 USD = {rate} LBP",
    "update_exchange_rate_label": "Update exchange rate (LBP per 1 USD)",
    "update_exchange_rate_button": "Update Exchange Rate",
    "exchange_rate_updated_success": "Exchange rate updated!",
    "budget_expander": "🎯 Monthly Budget Alert",
    "current_budget_text": "Current budget: ${threshold}",
    "no_budget_set": "No budget set.",
    "set_budget_label": "Set monthly budget ($)",
    "update_budget_button": "Update Budget",
    "budget_updated_success": "Budget updated!",
    "outage_schedule_expander": "🔌 Recurring Outage Schedule",
    "outage_schedule_description": (
        "If your grid outages follow a predictable daily pattern, set it once here "
        "instead of logging every outage individually."
    ),
    "current_schedule_text": "Current schedule: {hours} hours/day",
    "no_schedule_set": "No recurring schedule set.",
    "typical_outage_hours_label": "Typical outage hours per day",
    "update_schedule_button": "Update Schedule",
    "schedule_updated_success": "Outage schedule updated!",
    "delete_business_expander": "🗑️ Delete This Business",
    "delete_business_warning": (
        "This will permanently delete this business and ALL of its energy entries, "
        "outages, and recommendations. This cannot be undone."
    ),
    "delete_business_button": "Delete Business",
    "confirm_delete_business_text": "Are you absolutely sure you want to delete '{name}'?",
    "confirm_delete_yes": "Yes, delete everything",
    "business_deleted_success": "Business deleted.",
    "language_expander": "🌐 Language",
    "settings_expander": "⚙️ Settings",
    "language_select_label": "Display language",
    "update_language_button": "Update Language",
    "language_updated_success": "Language updated!",
    "generator_capacity_expander": "⚙️ Generator Capacity",
    "generator_capacity_description": (
        "Set your generator's rated capacity to enable load analysis in recommendations."
    ),
    "current_generator_capacity_text": "Current capacity: {capacity} kVA",
    "no_generator_capacity_set": "No generator capacity set.",
    "set_generator_capacity_label": "Generator capacity (kVA)",
    "update_generator_capacity_button": "Update Generator Capacity",
    "generator_capacity_updated_success": "Generator capacity updated!",
    "currently_working_with": "Currently working with: **{name}**",
    "use_sidebar_hint": "Use the sidebar to log a new entry or view your dashboard.",

    # 1_Log_Entry.py
    "log_entry_title": "📝 Log Energy Entry",
    "save_entry_button": "Save Entry",
    "entry_saved_success": "Entry saved!",
    "import_csv_header": "Import Entries from CSV",
    "import_csv_caption": (
        "Columns: date (YYYY-MM-DD), source (grid/generator/solar), "
        "currency (USD/LBP, optional, default USD), cost, units_kwh (optional), "
        "diesel_liters (optional), hours_run (optional), "
        "time_of_day (morning/afternoon/evening_night, optional, grid/generator only), "
        "notes (optional)"
    ),
    "choose_csv_label": "Choose a CSV file",
    "could_not_read_csv": "Could not read CSV: {error}",
    "preview_label": "Preview:",
    "import_entries_button": "Import Entries",
    "missing_required_field": "missing required field (date, source, or cost)",
    "invalid_date": "invalid date: {value}",
    "unrecognized_source": "unrecognized source: {value}",
    "unrecognized_currency": "unrecognized currency: {value}",
    "invalid_cost": "invalid cost: {value}",
    "unrecognized_time_of_day": "unrecognized time_of_day: {value}",
    "database_error_while_saving": "database error while saving",
    "imported_rows_success": "Imported {imported} of {total} row(s).",
    "skipped_rows_warning": "Skipped {count} row(s):",
    "row_column": "Row",
    "reason_column": "Reason",

    # 2_Dashboard.py
    "dashboard_title": "📊 Energy Cost Dashboard",
    "no_entries_info": "No entries logged yet. Head to 'Log Entry' to add your first one.",
    "total_cost_metric": "Total Cost",
    "entries_logged_metric": "Entries Logged",
    "sources_used_metric": "Sources Used",
    "over_budget_error": "⚠️ Over budget: spent ${spent} this month, budget is ${threshold}",
    "on_track_success": "✅ On track: ${spent} spent this month, ${remaining} remaining of your ${threshold} budget",
    "scheduled_outage_hours_metric": "Scheduled Outage Hours (this month)",
    "manually_logged_metric": "Manually Logged (this month)",
    "outage_overlap_caption": (
        "These are shown separately and never added together, since a scheduled estimate "
        "and a specific logged outage may overlap on the same day."
    ),
    "cost_efficiency_header": "Cost Efficiency by Source",
    "no_data_label": "No data",
    "cost_per_kwh_metric": "cost per kWh",
    "cost_per_hour_metric": "cost per hour",
    "grid_rate_header": "How Your Grid Rate Compares",
    "grid_rate_above": "Your grid rate (\\${value}/kWh) is above the typical range. Reference: {note}",
    "grid_rate_below": "Your grid rate (\\${value}/kWh) is below the typical range. Reference: {note}",
    "grid_rate_within": "Your grid rate (\\${value}/kWh) is within the typical range. Reference: {note}",
    "cost_by_source_header": "Cost by Source",
    "cost_over_time_header": "Cost Over Time",
    "outage_vs_generator_header": "Outage Hours vs. Generator Cost",
    "log_both_info": "Log both outages and generator entries to see this comparison.",
    "outage_hours_series": "Outage Hours",
    "generator_cost_series": "Generator Cost",
    "all_entries_header": "All Entries",
    "download_csv_button": "Download CSV",
    "download_pdf_button": "Download PDF Report",
    "edit_delete_header": "Edit or Delete an Entry",
    "select_entry_label": "Select an entry",
    "update_entry_button": "Update Entry",
    "entry_updated_success": "Entry updated!",
    "delete_entry_button": "Delete Entry",
    "confirm_delete_entry_warning": "Are you sure you want to delete this entry? This cannot be undone.",
    "yes_delete_it": "Yes, delete it",
    "entry_deleted_success": "Entry deleted!",

    # 3_Ask_AI.py
    "ask_ai_title": "🤖 Ask About Your Energy Costs",
    "ask_ai_chat_placeholder": "Ask a question about your energy costs...",

    # 4_Recommendations.py
    "recommendations_title": "💡 Cost-Saving Recommendations",
    "recommendations_intro": "Get an AI-generated recommendation on how to shift your energy usage to reduce costs.",
    "generate_recommendation_button": "Generate Recommendation",
    "analyzing_spinner": "Analyzing your energy data...",
    "past_recommendations_header": "Past Recommendations",
    "no_recommendations_info": "No recommendations generated yet.",
    "followed_yes_button": "I followed this",
    "followed_no_button": "I didn't follow this",
    "followed_caption": "✅ You followed this recommendation",
    "not_followed_caption": "⏭️ You didn't follow this recommendation",
    "impact_default_reason": "Not enough data to measure impact yet.",
    "impact_improved": (
        "Spending dropped from \\${before} to \\${after} the following month "
        "(saved \\${saved})"
    ),
    "impact_worsened": (
        "Spending went from \\${before} to \\${after} the following month "
        "(increased \\${increase})"
    ),

    # 5_Log_Outage.py
    "log_outage_title": "🔌 Log Grid Outage",
    "hours_without_power_label": "Hours without grid power",
    "log_outage_button": "Log Outage",
    "outage_logged_success": "Outage logged!",
    "outage_history_header": "Outage History",
    "no_outages_info": "No outages logged yet.",

    # 6_Solar_Payback.py
    "solar_payback_title": "☀️ Solar Payback Calculator",
    "solar_payback_intro": (
        "Estimate how many months it would take for additional solar capacity "
        "to pay for itself, based on your current grid cost per kWh."
    ),
    "upfront_cost_label": "Upfront cost of new solar capacity ($)",
    "estimate_method_label": "How do you want to estimate output?",
    "estimate_method_panels": "Number of panels",
    "estimate_method_kwh": "I know the kWh/day",
    "num_panels_label": "Number of new panels",
    "panel_estimate_caption": (
        "Estimated at {kwh} kWh/day, assuming {watts}W panels, "
        "{sun_hours} peak sun hours/day, {efficiency}% real-world efficiency."
    ),
    "extra_kwh_label": "Additional kWh per day this would produce",
    "calculate_payback_button": "Calculate Payback",
    "payback_not_possible_warning": (
        "Not enough data to calculate this. Make sure you've logged at least one "
        "grid entry, and that additional kWh per day is greater than zero."
    ),
    "estimated_monthly_savings_metric": "Estimated Monthly Savings",
    "payback_period_metric": "Payback Period",
    "months_suffix_value": "{months} months",

    # 7_What_If_Simulator.py
    "whatif_title": "🔮 What-If Savings Simulator",
    "whatif_intro": (
        "Explore hypothetical changes to your energy usage and see the projected "
        "monthly savings, based on your logged cost history."
    ),
    "scenario_inputs_header": "Scenario inputs",
    "generator_hours_reduction_label": "Run the generator this many fewer hours/day",
    "grid_to_solar_shift_label": "Shift this many kWh/day from grid to solar",
    "simulate_savings_button": "Simulate Savings",
    "simulation_not_possible_warning": (
        "Not enough data to calculate this. Make sure you've logged at least one "
        "entry for the sources involved, and that at least one scenario input is "
        "greater than zero."
    ),
    "generator_hours_savings_metric": "From fewer generator hours",
    "grid_shift_savings_metric": "From shifting grid to solar",
    "total_projected_savings_metric": "Total Projected Monthly Savings",
    "amount_per_month_value": "${amount}/mo",

    # Summary card (Dashboard)
    "download_summary_card_button": "Download Summary Card",
    "card_header_label": "Energy Cost Summary",
    "card_total_label": "Total This Month",
    "card_by_source_label": "This Month by Source",
    "card_footer_note": "Energy Cost Tracker",
    "summary_card_unavailable_arabic": "Summary card image is not yet available in Arabic.",
}

FR = {
    "no_business_warning": "Aucune entreprise sélectionnée. Veuillez d'abord vous rendre sur la page d'accueil.",
    "date_label": "Date",
    "notes_label": "Remarques (facultatif)",
    "cost_label": "Coût",
    "currency_label": "Devise",
    "energy_source_label": "Source d'énergie",
    "units_kwh_label": "Unités consommées (kWh)",
    "diesel_liters_label": "Diesel utilisé (litres)",
    "hours_run_label": "Heures de fonctionnement",
    "time_of_day_label": "Moment de la journée",
    "time_of_day_morning": "Matin",
    "time_of_day_afternoon": "Après-midi",
    "time_of_day_evening_night": "Soir/Nuit",
    "cancel_button": "Annuler",
    "total_outage_hours_metric": "Total des heures de coupure",
    "source_grid": "Réseau",
    "source_generator": "Générateur",
    "source_solar": "Solaire",

    "nav_home": "Accueil",
    "nav_log_entry": "Enregistrer une entrée",
    "nav_dashboard": "Tableau de bord",
    "nav_ask_ai": "Demander à l'IA",
    "nav_recommendations": "Recommandations",
    "nav_log_outage": "Enregistrer une coupure",
    "nav_solar_payback": "Rentabilité solaire",
    "nav_whatif": "Simulateur hypothétique",

    "app_title": "⚡ Suivi des coûts énergétiques",
    "app_subtitle": "Suivez et comprenez les coûts énergétiques de votre entreprise entre réseau, générateur et solaire.",
    "active_business_label": "Entreprise active",
    "add_business_expander": "➕ Ajouter une nouvelle entreprise",
    "business_name_label": "Nom de l'entreprise",
    "create_business_button": "Créer l'entreprise",
    "enter_business_name_warning": "Veuillez saisir un nom d'entreprise.",
    "exchange_rate_expander": "💱 Paramètres du taux de change",
    "current_rate_text": "Taux actuel : 1 USD = {rate} LBP",
    "update_exchange_rate_label": "Mettre à jour le taux de change (LBP pour 1 USD)",
    "update_exchange_rate_button": "Mettre à jour le taux de change",
    "exchange_rate_updated_success": "Taux de change mis à jour !",
    "budget_expander": "🎯 Alerte de budget mensuel",
    "current_budget_text": "Budget actuel : ${threshold}",
    "no_budget_set": "Aucun budget défini.",
    "set_budget_label": "Définir le budget mensuel ($)",
    "update_budget_button": "Mettre à jour le budget",
    "budget_updated_success": "Budget mis à jour !",
    "outage_schedule_expander": "🔌 Programme de coupures récurrentes",
    "outage_schedule_description": (
        "Si les coupures de votre réseau suivent un schéma quotidien prévisible, "
        "définissez-le une fois ici plutôt que d'enregistrer chaque coupure individuellement."
    ),
    "current_schedule_text": "Programme actuel : {hours} heures/jour",
    "no_schedule_set": "Aucun programme récurrent défini.",
    "typical_outage_hours_label": "Heures de coupure habituelles par jour",
    "update_schedule_button": "Mettre à jour le programme",
    "schedule_updated_success": "Programme de coupures mis à jour !",
    "delete_business_expander": "🗑️ Supprimer cette entreprise",
    "delete_business_warning": (
        "Cela supprimera définitivement cette entreprise et TOUTES ses entrées d'énergie, "
        "coupures et recommandations. Cette action est irréversible."
    ),
    "delete_business_button": "Supprimer l'entreprise",
    "confirm_delete_business_text": "Êtes-vous absolument sûr de vouloir supprimer « {name} » ?",
    "language_expander": "🌐 Langue",
    "settings_expander": "⚙️ Paramètres",
    "confirm_delete_yes": "Oui, tout supprimer",
    "business_deleted_success": "Entreprise supprimée.",
    "language_select_label": "Langue d'affichage",
    "update_language_button": "Mettre à jour la langue",
    "language_updated_success": "Langue mise à jour !",
    "generator_capacity_expander": "⚙️ Capacité du générateur",
    "generator_capacity_description": (
        "Définissez la capacité nominale de votre générateur pour activer l'analyse de "
        "charge dans les recommandations."
    ),
    "current_generator_capacity_text": "Capacité actuelle : {capacity} kVA",
    "no_generator_capacity_set": "Aucune capacité de générateur définie.",
    "set_generator_capacity_label": "Capacité du générateur (kVA)",
    "update_generator_capacity_button": "Mettre à jour la capacité",
    "generator_capacity_updated_success": "Capacité du générateur mise à jour !",
    "currently_working_with": "Entreprise actuelle : **{name}**",
    "use_sidebar_hint": "Utilisez la barre latérale pour enregistrer une nouvelle entrée ou consulter votre tableau de bord.",

    "log_entry_title": "📝 Enregistrer une entrée d'énergie",
    "save_entry_button": "Enregistrer l'entrée",
    "entry_saved_success": "Entrée enregistrée !",
    "import_csv_header": "Importer des entrées depuis un CSV",
    "import_csv_caption": (
        "Colonnes : date (AAAA-MM-JJ), source (grid/generator/solar), "
        "currency (USD/LBP, facultatif, USD par défaut), cost, units_kwh (facultatif), "
        "diesel_liters (facultatif), hours_run (facultatif), "
        "time_of_day (morning/afternoon/evening_night, facultatif, grid/generator uniquement), "
        "notes (facultatif)"
    ),
    "choose_csv_label": "Choisir un fichier CSV",
    "could_not_read_csv": "Impossible de lire le CSV : {error}",
    "preview_label": "Aperçu :",
    "import_entries_button": "Importer les entrées",
    "missing_required_field": "champ requis manquant (date, source ou cost)",
    "invalid_date": "date invalide : {value}",
    "unrecognized_source": "source non reconnue : {value}",
    "unrecognized_currency": "devise non reconnue : {value}",
    "invalid_cost": "coût invalide : {value}",
    "unrecognized_time_of_day": "time_of_day non reconnu : {value}",
    "database_error_while_saving": "erreur de base de données lors de l'enregistrement",
    "imported_rows_success": "{imported} ligne(s) importée(s) sur {total}.",
    "skipped_rows_warning": "{count} ligne(s) ignorée(s) :",
    "row_column": "Ligne",
    "reason_column": "Raison",

    "dashboard_title": "📊 Tableau de bord des coûts énergétiques",
    "no_entries_info": "Aucune entrée enregistrée pour le moment. Rendez-vous sur « Log Entry » pour ajouter la première.",
    "total_cost_metric": "Coût total",
    "entries_logged_metric": "Entrées enregistrées",
    "sources_used_metric": "Sources utilisées",
    "over_budget_error": "⚠️ Budget dépassé : ${spent} dépensés ce mois-ci, budget de ${threshold}",
    "on_track_success": "✅ Dans les limites : ${spent} dépensés ce mois-ci, ${remaining} restants sur votre budget de ${threshold}",
    "scheduled_outage_hours_metric": "Heures de coupure programmées (ce mois-ci)",
    "manually_logged_metric": "Enregistrées manuellement (ce mois-ci)",
    "outage_overlap_caption": (
        "Ces valeurs sont affichées séparément et jamais additionnées, car une estimation "
        "programmée et une coupure enregistrée spécifique peuvent se chevaucher le même jour."
    ),
    "cost_efficiency_header": "Efficacité des coûts par source",
    "no_data_label": "Aucune donnée",
    "cost_per_kwh_metric": "coût par kWh",
    "cost_per_hour_metric": "coût par heure",
    "grid_rate_header": "Comparaison de votre tarif réseau",
    "grid_rate_above": "Votre tarif réseau (\\${value}/kWh) est supérieur à la fourchette habituelle. Référence : {note}",
    "grid_rate_below": "Votre tarif réseau (\\${value}/kWh) est inférieur à la fourchette habituelle. Référence : {note}",
    "grid_rate_within": "Votre tarif réseau (\\${value}/kWh) se situe dans la fourchette habituelle. Référence : {note}",
    "cost_by_source_header": "Coût par source",
    "cost_over_time_header": "Coût dans le temps",
    "outage_vs_generator_header": "Heures de coupure vs coût du générateur",
    "log_both_info": "Enregistrez à la fois des coupures et des entrées de générateur pour voir cette comparaison.",
    "outage_hours_series": "Heures de coupure",
    "generator_cost_series": "Coût du générateur",
    "all_entries_header": "Toutes les entrées",
    "download_csv_button": "Télécharger le CSV",
    "download_pdf_button": "Télécharger le rapport PDF",
    "edit_delete_header": "Modifier ou supprimer une entrée",
    "select_entry_label": "Sélectionner une entrée",
    "update_entry_button": "Mettre à jour l'entrée",
    "entry_updated_success": "Entrée mise à jour !",
    "delete_entry_button": "Supprimer l'entrée",
    "confirm_delete_entry_warning": "Êtes-vous sûr de vouloir supprimer cette entrée ? Cette action est irréversible.",
    "yes_delete_it": "Oui, supprimer",
    "entry_deleted_success": "Entrée supprimée !",

    "ask_ai_title": "🤖 Interrogez vos coûts énergétiques",
    "ask_ai_chat_placeholder": "Posez une question sur vos coûts énergétiques...",

    "recommendations_title": "💡 Recommandations d'économies",
    "recommendations_intro": (
        "Obtenez une recommandation générée par IA sur la façon de réajuster votre "
        "consommation d'énergie pour réduire les coûts."
    ),
    "generate_recommendation_button": "Générer une recommandation",
    "analyzing_spinner": "Analyse de vos données énergétiques...",
    "past_recommendations_header": "Recommandations précédentes",
    "no_recommendations_info": "Aucune recommandation générée pour le moment.",
    "followed_yes_button": "J'ai suivi cette recommandation",
    "followed_no_button": "Je n'ai pas suivi cette recommandation",
    "followed_caption": "✅ Vous avez suivi cette recommandation",
    "not_followed_caption": "⏭️ Vous n'avez pas suivi cette recommandation",
    "impact_default_reason": "Pas encore assez de données pour mesurer l'impact.",
    "impact_improved": (
        "Les dépenses sont passées de \\${before} à \\${after} le mois suivant "
        "(économie de \\${saved})"
    ),
    "impact_worsened": (
        "Les dépenses sont passées de \\${before} à \\${after} le mois suivant "
        "(augmentation de \\${increase})"
    ),

    "log_outage_title": "🔌 Enregistrer une coupure de réseau",
    "hours_without_power_label": "Heures sans électricité du réseau",
    "log_outage_button": "Enregistrer la coupure",
    "outage_logged_success": "Coupure enregistrée !",
    "outage_history_header": "Historique des coupures",
    "no_outages_info": "Aucune coupure enregistrée pour le moment.",

    "solar_payback_title": "☀️ Calculateur de rentabilité solaire",
    "solar_payback_intro": (
        "Estimez le nombre de mois nécessaires pour que la capacité solaire supplémentaire "
        "s'autofinance, en fonction de votre coût actuel du réseau par kWh."
    ),
    "upfront_cost_label": "Coût initial de la nouvelle capacité solaire ($)",
    "estimate_method_label": "Comment souhaitez-vous estimer la production ?",
    "estimate_method_panels": "Nombre de panneaux",
    "estimate_method_kwh": "Je connais les kWh/jour",
    "num_panels_label": "Nombre de nouveaux panneaux",
    "panel_estimate_caption": (
        "Estimé à {kwh} kWh/jour, en supposant des panneaux de {watts}W, "
        "{sun_hours} heures d'ensoleillement maximal par jour, et une efficacité réelle de {efficiency}%."
    ),
    "extra_kwh_label": "kWh supplémentaires par jour que cela produirait",
    "calculate_payback_button": "Calculer la rentabilité",
    "payback_not_possible_warning": (
        "Pas assez de données pour calculer cela. Assurez-vous d'avoir enregistré au moins "
        "une entrée réseau, et que les kWh supplémentaires par jour sont supérieurs à zéro."
    ),
    "estimated_monthly_savings_metric": "Économies mensuelles estimées",
    "payback_period_metric": "Période de rentabilité",
    "months_suffix_value": "{months} mois",

    "whatif_title": "🔮 Simulateur d'économies hypothétiques",
    "whatif_intro": (
        "Explorez des changements hypothétiques dans votre consommation d'énergie et "
        "visualisez les économies mensuelles projetées, en fonction de votre historique de coûts enregistré."
    ),
    "scenario_inputs_header": "Paramètres du scénario",
    "generator_hours_reduction_label": "Faire fonctionner le générateur ce nombre d'heures en moins par jour",
    "grid_to_solar_shift_label": "Transférer ce nombre de kWh par jour du réseau vers le solaire",
    "simulate_savings_button": "Simuler les économies",
    "simulation_not_possible_warning": (
        "Pas assez de données pour calculer cela. Assurez-vous d'avoir enregistré au moins "
        "une entrée pour les sources concernées, et qu'au moins un paramètre du scénario "
        "est supérieur à zéro."
    ),
    "generator_hours_savings_metric": "Grâce à moins d'heures de générateur",
    "grid_shift_savings_metric": "Grâce au transfert du réseau vers le solaire",
    "total_projected_savings_metric": "Total des économies mensuelles projetées",
    "amount_per_month_value": "${amount}/mois",

    "download_summary_card_button": "Télécharger la carte résumé",
    "card_header_label": "Résumé des coûts énergétiques",
    "card_total_label": "Total ce mois-ci",
    "card_by_source_label": "Ce mois-ci par source",
    "card_footer_note": "Suivi des coûts énergétiques",
    "summary_card_unavailable_arabic": "L'image de la carte résumé n'est pas encore disponible en arabe.",
}

AR = {
    "no_business_warning": "لم يتم اختيار أي منشأة. يرجى الانتقال إلى الصفحة الرئيسية أولاً.",
    "date_label": "التاريخ",
    "notes_label": "ملاحظات (اختياري)",
    "cost_label": "التكلفة",
    "currency_label": "العملة",
    "energy_source_label": "مصدر الطاقة",
    "units_kwh_label": "الوحدات المستهلكة (كيلوواط/ساعة)",
    "diesel_liters_label": "الديزل المستخدم (لتر)",
    "hours_run_label": "ساعات التشغيل",
    "time_of_day_label": "وقت اليوم",
    "time_of_day_morning": "الصباح",
    "time_of_day_afternoon": "بعد الظهر",
    "time_of_day_evening_night": "المساء/الليل",
    "cancel_button": "إلغاء",
    "total_outage_hours_metric": "إجمالي ساعات الانقطاع",
    "source_grid": "الشبكة",
    "source_generator": "المولد",
    "source_solar": "الطاقة الشمسية",

    "nav_home": "الرئيسية",
    "nav_log_entry": "تسجيل إدخال",
    "nav_dashboard": "لوحة التحكم",
    "nav_ask_ai": "اسأل الذكاء الاصطناعي",
    "nav_recommendations": "التوصيات",
    "nav_log_outage": "تسجيل انقطاع",
    "nav_solar_payback": "استرداد التكلفة الشمسية",
    "nav_whatif": "المحاكي الافتراضي",

    "app_title": "⚡ متتبع تكاليف الطاقة",
    "app_subtitle": "تتبّع وافهم تكاليف الطاقة في منشأتك عبر الشبكة والمولد والطاقة الشمسية.",
    "active_business_label": "المنشأة النشطة",
    "add_business_expander": "➕ إضافة منشأة جديدة",
    "business_name_label": "اسم المنشأة",
    "create_business_button": "إنشاء المنشأة",
    "enter_business_name_warning": "يرجى إدخال اسم المنشأة.",
    "exchange_rate_expander": "💱 إعدادات سعر الصرف",
    "current_rate_text": "السعر الحالي: 1 دولار أمريكي = {rate} ليرة لبنانية",
    "update_exchange_rate_label": "تحديث سعر الصرف (ليرة لبنانية مقابل 1 دولار)",
    "update_exchange_rate_button": "تحديث سعر الصرف",
    "exchange_rate_updated_success": "تم تحديث سعر الصرف!",
    "budget_expander": "🎯 تنبيه الميزانية الشهرية",
    "current_budget_text": "الميزانية الحالية: ${threshold}",
    "no_budget_set": "لم يتم تحديد ميزانية.",
    "set_budget_label": "تحديد الميزانية الشهرية ($)",
    "update_budget_button": "تحديث الميزانية",
    "budget_updated_success": "تم تحديث الميزانية!",
    "outage_schedule_expander": "🔌 جدول الانقطاعات المتكررة",
    "outage_schedule_description": (
        "إذا كانت انقطاعات الشبكة لديك تتبع نمطاً يومياً متوقعاً، يمكنك تحديده مرة واحدة "
        "هنا بدلاً من تسجيل كل انقطاع على حدة."
    ),
    "current_schedule_text": "الجدول الحالي: {hours} ساعة/يوم",
    "no_schedule_set": "لا يوجد جدول متكرر محدد.",
    "typical_outage_hours_label": "ساعات الانقطاع المعتادة يومياً",
    "update_schedule_button": "تحديث الجدول",
    "schedule_updated_success": "تم تحديث جدول الانقطاعات!",
    "delete_business_expander": "🗑️ حذف هذه المنشأة",
    "delete_business_warning": (
        "سيؤدي هذا إلى حذف هذه المنشأة نهائياً مع جميع إدخالات الطاقة والانقطاعات "
        "والتوصيات الخاصة بها. لا يمكن التراجع عن هذا الإجراء."
    ),
    "delete_business_button": "حذف المنشأة",
    "language_expander": "🌐 اللغة",
    "settings_expander": "⚙️ الإعدادات",
    "confirm_delete_business_text": "هل أنت متأكد تماماً من رغبتك في حذف '{name}'؟",
    "confirm_delete_yes": "نعم، احذف كل شيء",
    "business_deleted_success": "تم حذف المنشأة.",
    "language_select_label": "لغة العرض",
    "update_language_button": "تحديث اللغة",
    "language_updated_success": "تم تحديث اللغة!",
    "generator_capacity_expander": "⚙️ سعة المولد",
    "generator_capacity_description": "حدّد السعة الاسمية لمولدك لتفعيل تحليل الحمل في التوصيات.",
    "current_generator_capacity_text": "السعة الحالية: {capacity} كيلوفولت أمبير",
    "no_generator_capacity_set": "لم يتم تحديد سعة المولد.",
    "set_generator_capacity_label": "سعة المولد (كيلوفولت أمبير)",
    "update_generator_capacity_button": "تحديث سعة المولد",
    "generator_capacity_updated_success": "تم تحديث سعة المولد!",
    "currently_working_with": "تعمل حالياً مع: **{name}**",
    "use_sidebar_hint": "استخدم الشريط الجانبي لتسجيل إدخال جديد أو عرض لوحة التحكم الخاصة بك.",

    "log_entry_title": "📝 تسجيل إدخال طاقة",
    "save_entry_button": "حفظ الإدخال",
    "entry_saved_success": "تم حفظ الإدخال!",
    "import_csv_header": "استيراد الإدخالات من ملف CSV",
    "import_csv_caption": (
        "الأعمدة: date (YYYY-MM-DD)، source (grid/generator/solar)، "
        "currency (USD/LBP، اختياري، الافتراضي USD)، cost، units_kwh (اختياري)، "
        "diesel_liters (اختياري)، hours_run (اختياري)، "
        "time_of_day (morning/afternoon/evening_night، اختياري، للشبكة والمولد فقط)، "
        "notes (اختياري)"
    ),
    "choose_csv_label": "اختر ملف CSV",
    "could_not_read_csv": "تعذّرت قراءة ملف CSV: {error}",
    "preview_label": "معاينة:",
    "import_entries_button": "استيراد الإدخالات",
    "missing_required_field": "حقل مطلوب مفقود (date أو source أو cost)",
    "invalid_date": "تاريخ غير صالح: {value}",
    "unrecognized_source": "مصدر غير معروف: {value}",
    "unrecognized_currency": "عملة غير معروفة: {value}",
    "invalid_cost": "تكلفة غير صالحة: {value}",
    "unrecognized_time_of_day": "قيمة time_of_day غير معروفة: {value}",
    "database_error_while_saving": "خطأ في قاعدة البيانات أثناء الحفظ",
    "imported_rows_success": "تم استيراد {imported} من أصل {total} صف/صفوف.",
    "skipped_rows_warning": "تم تخطي {count} صف/صفوف:",
    "row_column": "الصف",
    "reason_column": "السبب",

    "dashboard_title": "📊 لوحة تحكم تكاليف الطاقة",
    "no_entries_info": "لا توجد إدخالات مسجلة بعد. توجّه إلى 'Log Entry' لإضافة أول إدخال.",
    "total_cost_metric": "التكلفة الإجمالية",
    "entries_logged_metric": "الإدخالات المسجلة",
    "sources_used_metric": "المصادر المستخدمة",
    "over_budget_error": "⚠️ تجاوز الميزانية: تم إنفاق ${spent} هذا الشهر، والميزانية ${threshold}",
    "on_track_success": "✅ ضمن الحدود: تم إنفاق ${spent} هذا الشهر، ويتبقى ${remaining} من ميزانيتك البالغة ${threshold}",
    "scheduled_outage_hours_metric": "ساعات الانقطاع المجدولة (هذا الشهر)",
    "manually_logged_metric": "المسجلة يدوياً (هذا الشهر)",
    "outage_overlap_caption": (
        "تُعرض هذه القيم بشكل منفصل ولا تُجمع أبداً، لأن التقدير المجدول والانقطاع "
        "المسجل قد يتداخلان في نفس اليوم."
    ),
    "cost_efficiency_header": "كفاءة التكلفة حسب المصدر",
    "no_data_label": "لا توجد بيانات",
    "cost_per_kwh_metric": "التكلفة لكل كيلوواط/ساعة",
    "cost_per_hour_metric": "التكلفة لكل ساعة",
    "grid_rate_header": "مقارنة تعرفة الشبكة الخاصة بك",
    "grid_rate_above": "تعرفة الشبكة لديك (\\${value}/كيلوواط ساعة) أعلى من النطاق المعتاد. المرجع: {note}",
    "grid_rate_below": "تعرفة الشبكة لديك (\\${value}/كيلوواط ساعة) أقل من النطاق المعتاد. المرجع: {note}",
    "grid_rate_within": "تعرفة الشبكة لديك (\\${value}/كيلوواط ساعة) ضمن النطاق المعتاد. المرجع: {note}",
    "cost_by_source_header": "التكلفة حسب المصدر",
    "cost_over_time_header": "التكلفة عبر الزمن",
    "outage_vs_generator_header": "ساعات الانقطاع مقابل تكلفة المولد",
    "log_both_info": "سجّل كلاً من الانقطاعات وإدخالات المولد لعرض هذه المقارنة.",
    "outage_hours_series": "ساعات الانقطاع",
    "generator_cost_series": "تكلفة المولد",
    "all_entries_header": "جميع الإدخالات",
    "download_csv_button": "تنزيل CSV",
    "download_pdf_button": "تنزيل تقرير PDF",
    "edit_delete_header": "تعديل أو حذف إدخال",
    "select_entry_label": "اختر إدخالاً",
    "update_entry_button": "تحديث الإدخال",
    "entry_updated_success": "تم تحديث الإدخال!",
    "delete_entry_button": "حذف الإدخال",
    "confirm_delete_entry_warning": "هل أنت متأكد من رغبتك في حذف هذا الإدخال؟ لا يمكن التراجع عن هذا الإجراء.",
    "yes_delete_it": "نعم، احذفه",
    "entry_deleted_success": "تم حذف الإدخال!",

    "ask_ai_title": "🤖 اسأل عن تكاليف طاقتك",
    "ask_ai_chat_placeholder": "اطرح سؤالاً حول تكاليف طاقتك...",

    "recommendations_title": "💡 توصيات لتوفير التكاليف",
    "recommendations_intro": (
        "احصل على توصية مُولّدة بالذكاء الاصطناعي حول كيفية تعديل استهلاكك للطاقة "
        "لخفض التكاليف."
    ),
    "generate_recommendation_button": "توليد توصية",
    "analyzing_spinner": "جارٍ تحليل بيانات الطاقة الخاصة بك...",
    "past_recommendations_header": "التوصيات السابقة",
    "no_recommendations_info": "لم يتم توليد أي توصيات بعد.",
    "followed_yes_button": "لقد اتبعت هذه التوصية",
    "followed_no_button": "لم أتبع هذه التوصية",
    "followed_caption": "✅ لقد اتبعت هذه التوصية",
    "not_followed_caption": "⏭️ لم تتبع هذه التوصية",
    "impact_default_reason": "لا توجد بيانات كافية بعد لقياس الأثر.",
    "impact_improved": (
        "انخفض الإنفاق من \\${before} إلى \\${after} في الشهر التالي (توفير \\${saved})"
    ),
    "impact_worsened": (
        "ارتفع الإنفاق من \\${before} إلى \\${after} في الشهر التالي (زيادة \\${increase})"
    ),

    "log_outage_title": "🔌 تسجيل انقطاع الشبكة",
    "hours_without_power_label": "ساعات انقطاع كهرباء الشبكة",
    "log_outage_button": "تسجيل الانقطاع",
    "outage_logged_success": "تم تسجيل الانقطاع!",
    "outage_history_header": "سجل الانقطاعات",
    "no_outages_info": "لا توجد انقطاعات مسجلة بعد.",

    "solar_payback_title": "☀️ حاسبة استرداد تكلفة الطاقة الشمسية",
    "solar_payback_intro": (
        "قدّر عدد الأشهر التي تحتاجها السعة الشمسية الإضافية لتغطية تكلفتها، بناءً على "
        "تكلفة الشبكة الحالية لكل كيلوواط/ساعة."
    ),
    "upfront_cost_label": "التكلفة الأولية للسعة الشمسية الجديدة ($)",
    "estimate_method_label": "كيف تريد تقدير الإنتاج؟",
    "estimate_method_panels": "عدد الألواح",
    "estimate_method_kwh": "أعرف الكيلوواط/ساعة يومياً",
    "num_panels_label": "عدد الألواح الجديدة",
    "panel_estimate_caption": (
        "تقدير {kwh} كيلوواط/ساعة يومياً، بافتراض ألواح بقدرة {watts} واط، "
        "و{sun_hours} ساعة ذروة شمسية يومياً، وكفاءة فعلية {efficiency}%."
    ),
    "extra_kwh_label": "الكيلوواط/ساعة الإضافية التي سينتجها هذا يومياً",
    "calculate_payback_button": "حساب فترة الاسترداد",
    "payback_not_possible_warning": (
        "لا توجد بيانات كافية لحساب هذا. تأكد من أنك سجلت إدخالاً واحداً على الأقل "
        "للشبكة، وأن الكيلوواط/ساعة الإضافية يومياً أكبر من صفر."
    ),
    "estimated_monthly_savings_metric": "التوفير الشهري المقدّر",
    "payback_period_metric": "فترة الاسترداد",
    "months_suffix_value": "{months} أشهر",

    "whatif_title": "🔮 محاكي التوفير الافتراضي",
    "whatif_intro": (
        "استكشف تغييرات افتراضية في استهلاكك للطاقة وشاهد التوفير الشهري المتوقع، "
        "بناءً على سجل تكاليفك المسجل."
    ),
    "scenario_inputs_header": "مدخلات السيناريو",
    "generator_hours_reduction_label": "تشغيل المولد لعدد أقل من الساعات يومياً",
    "grid_to_solar_shift_label": "نقل هذا العدد من الكيلوواط/ساعة يومياً من الشبكة إلى الطاقة الشمسية",
    "simulate_savings_button": "محاكاة التوفير",
    "simulation_not_possible_warning": (
        "لا توجد بيانات كافية لحساب هذا. تأكد من أنك سجلت إدخالاً واحداً على الأقل "
        "للمصادر المعنية، وأن أحد مدخلات السيناريو على الأقل أكبر من صفر."
    ),
    "generator_hours_savings_metric": "من تقليل ساعات المولد",
    "grid_shift_savings_metric": "من النقل من الشبكة إلى الطاقة الشمسية",
    "total_projected_savings_metric": "إجمالي التوفير الشهري المتوقع",
    "amount_per_month_value": "${amount}/شهرياً",

    "download_summary_card_button": "تنزيل بطاقة الملخص",
    "card_header_label": "ملخص تكاليف الطاقة",
    "card_total_label": "الإجمالي هذا الشهر",
    "card_by_source_label": "هذا الشهر حسب المصدر",
    "card_footer_note": "متتبع تكاليف الطاقة",
    "summary_card_unavailable_arabic": "صورة بطاقة الملخص غير متوفرة بعد باللغة العربية.",
}

MONTH_NAMES = {
    "en": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ],
    "fr": [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
    ],
    # Levantine month names, as commonly used in Lebanon (rather than the
    # transliterated Gregorian names used elsewhere in the Arab world).
    "ar": [
        "كانون الثاني", "شباط", "آذار", "نيسان", "أيار", "حزيران",
        "تموز", "آب", "أيلول", "تشرين الأول", "تشرين الثاني", "كانون الأول",
    ],
}


def month_name(month: int, language: str = "en") -> str:
    names = MONTH_NAMES.get(language, MONTH_NAMES["en"])
    return names[month - 1]


TRANSLATIONS = {"en": EN, "fr": FR, "ar": AR}


def t(key: str, language: str = "en", **kwargs) -> str:
    lang_dict = TRANSLATIONS.get(language, EN)
    template = lang_dict.get(key, EN.get(key, key))
    return template.format(**kwargs) if kwargs else template
