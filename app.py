import streamlit as st
from src.ui.navigation import render_navigation

pg = render_navigation()
pg.run()