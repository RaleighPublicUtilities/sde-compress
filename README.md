# sde-compress
Occasional job that compresses the database. It should be run weekly or more frequently. IndexingStatsOnly.py has the Archiving and Compress funtions commented out so that only the Rebuild Indexes and Analyze Datasets tools run. IndexingStatsOnly can be run at any time. ArchiveAndCompress can only be run when there are no schema locks on the database.
