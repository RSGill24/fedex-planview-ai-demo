-- Replace ${PROJECT_ID} with your project ID or run through envsubst.
CREATE SCHEMA IF NOT EXISTS `${PROJECT_ID}.planview_raw` OPTIONS(location="${BQ_LOCATION}");
CREATE SCHEMA IF NOT EXISTS `${PROJECT_ID}.planview_silver` OPTIONS(location="${BQ_LOCATION}");
CREATE SCHEMA IF NOT EXISTS `${PROJECT_ID}.planview_gold` OPTIONS(location="${BQ_LOCATION}");
CREATE SCHEMA IF NOT EXISTS `${PROJECT_ID}.planview_metadata` OPTIONS(location="${BQ_LOCATION}");
