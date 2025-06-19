create schema ZohoUS
GO 

/****** Object:  Table [ZohoUS].[LastSync]    Script Date: 17-06-2025 17:51:04 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [ZohoUS].[LastSync](
	[module] [varchar](255) NOT NULL,
	[sync_type] [varchar](255) NOT NULL,
	[last_sync_time] [datetime] NOT NULL,
 CONSTRAINT [PK_LastSync] PRIMARY KEY CLUSTERED 
(
	[module] ASC,
	[sync_type] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [ZohoUS].[LastSync] ADD  DEFAULT (getdate()) FOR [last_sync_time]
GO


/****** Object:  Table [ZohoUS].[ZohoAuth]    Script Date: 17-06-2025 17:52:55 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [ZohoUS].[ZohoAuth](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[access_token] [varchar](500) NULL,
	[refresh_token] [varchar](500) NULL,
	[expires_in] [int] NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [ZohoUS].[ZohoAuth] ADD  DEFAULT (getdate()) FOR [created_at]
GO