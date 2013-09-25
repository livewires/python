%% ----------------------------------------------------------------------
%%
%% wsheet.cls
%%
%% MJ White 1999
%% Worksheet class file for LiveWires teaching materials
%%
%% ----------------------------------------------------------------------

%% Disclaimer:
%% Yeah, I know it's pretty icky. :-)
%% I apologise to LaTeX-ies that I've gone and used TeX primitives all
%% over.  Sleep seemed more important at the time...

%% Modified:
%%          MJ White 11.05.2001 - Reworked for Adobe fonts

%% IMPORTANT:
%% If you are writing LiveWires material using this file, PLEASE DON'T 
%% MODIFY IT in isolation, or it'll be impossible to manage
%% worksheets.  If you have good ideas or good code to add, cool;
%% but please get in touch with me and I'll try and integrate them 
%% in an organised way.

%% Copyright Mark White. All rights reserved.
%% 
%% Redistribution and use, with or without modification, are permitted
%% provided that the following conditions are met:
%% 
%% Redistributions of this code must retain the above copyright notice,
%% this list of conditions and the following disclaimer.
%% 
%% Neither name of Scripture Union nor LiveWires nor the names of its
%% contributors may be used to endorse or promote products derived from
%% this software without specific prior written permission.
%% 
%% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
%% ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
%% LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
%% A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SCRIPTURE UNION
%% OR THE CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
%% SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
%% LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
%% DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
%% THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
%% (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
%% OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%% preamble: setup, options, etc

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{wsheet}[2001/05/10 v0.2
Live Wires worksheet document class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

%% packages

\LoadClass[a4paper]{article}
\RequirePackage{alltt}
\RequirePackage{calc}
\RequirePackage{fancyhdr}
\RequirePackage{ulem}
\RequirePackage{times}

%% ----------------------------------------------------------------------
%% main code

%% Setup

\parindent 0cm
\parskip 0.3cm
\textwidth 17.3cm
\textheight 24cm
\oddsidemargin -0.5cm
\evensidemargin -2cm
\topmargin -1.5cm
\headheight 1cm
\headsep 1cm

\pagestyle{fancyplain}

\normalem

%% Fonts for verbatim

\font\ProgramFont pcrr at 9pt
\font\LocalProgramFont pcrr at 10pt

%% If you prefer Adobe fonts, but can't stand courier (which would be
%% fair enough), try this instead:
% \font\ProgramFont cmtt10 at 9pt


%% title, author, date

\newcommand{\ws@author}[0]{}
\newcommand{\ws@long}[0]{}
\newcommand{\ws@short}[0]{}
\newcommand{\ws@date}[0]{}

\renewcommand{\author}[1]{%
  \renewcommand{\ws@author}[0]{#1}}
\renewcommand{\date}[1]{%
  \renewcommand{\ws@date}[0]{#1}}
\newcommand{\sheet}[2]{%
  \renewcommand{\ws@short}[0]{#1}%
  \renewcommand{\ws@long}[0]{#2}}

\rhead[{\slseries \ws@short}]{{\itshape \ws@long}}
\lhead[{\slseries \ws@long}]{{\itshape \ws@short}}
\cfoot{-- Page \thepage\ --}

%% key

\newcommand{\key}[1]{\thinspace\fbox{\LocalProgramFont #1}\thinspace}

%% note environment

\newlength{\@@notewidth}
\setlength{\@@notewidth}{\textwidth-3cm}
\newsavebox{\@@wsNote}
\newenvironment{note}[0]
  %% Start def
  {\begin{lrbox}{\@@wsNote}%
    \slshape \begin{minipage}[t]{\@@notewidth}}
  {\end{minipage}%
    \end{lrbox}%
    \vspace{0.3cm}%
    \centerline{%
      \fbox{\usebox{\@@wsNote}}%
      }%
    \vspace{0.3cm}}


%% trythis environment

\newlength{\trybarwidth}
\setlength{\trybarwidth}{0.4mm}

\newlength{\@@trywidth}
\newlength{\@@trywidthxx}
\newlength{\@@tryheight}
\newlength{\@@tryheightx}
\newlength{\@@trydepth}
\newsavebox{\@@wsTry}
\newenvironment{trythis}[0]
  %% Start def
  { \setlength{\@@trywidth}{\textwidth-3cm}
    \setlength{\@@trywidthxx}{\@@trywidth+4pt}
    \begin{lrbox}{\@@wsTry}%
    \begin{minipage}[t]{\@@trywidth}}
  { \end{minipage}%
    \end{lrbox}%
    \vspace{0.3cm}%
      \settoheight{\@@tryheight}{\usebox{\@@wsTry}}%
      \settodepth{\@@trydepth}{\usebox{\@@wsTry}}%
      \addtolength{\@@tryheight}{\@@trydepth}%
      \addtolength{\@@tryheight}{4pt}%
      \setlength{\@@tryheightx}{\@@tryheight-9.5pt}
      \hspace{0.8cm}%
      \rule[-\@@tryheightx]{\trybarwidth}{\@@tryheight}%
      \hspace{0.6cm}%
      \parbox[t]{\@@trywidthxx}{\usebox{\@@wsTry}}%
    \vspace{0.3cm}}


%% Verbatim environment stuff

%% Make vertical bar an active character, and define it.
%% I know the TeX way to do this; what's the LaTeX way?
\catcode`\|=\active
{\obeylines\gdef|{\ttverbatim\let^^M=\ \let|=\endgroup}}

\chardef\other=12
\def\ttverbatim{\begingroup %
%% We'll leave these characters special so that || behaves in the 
%% same way as the program environment, unless somewhat wants different!
%% \catcode`\\=\other \catcode`\{=\other \catcode`\}=\other
  \catcode`\$=\other \catcode`\&=\other \catcode`\#=\other %
  \catcode`\%=\other \catcode`\~=\other \catcode`\_=\other %
  \catcode`\^=\other %
  \def\\{\char'134}% % Backslash
  \def\|{\char'174}% % Vert bar
  \let\T=\@@T %      % Interactions
   \obeylines\LocalProgramFont\obeyspaces}

%% Make spaces do the right thing when active (i.e., when \obeyspaces).
{\obeyspaces\gdef {\ }}

%% Program environment

%% Comment command

\font\CommentFont ptmri at 9pt

\newlength{\cmtlength}
\newlength{\defcmtlength}
\newlength{\sidebarwidth}
\setlength{\cmtlength}{6cm}
\setlength{\defcmtlength}{6cm}
\setlength{\sidebarwidth}{0mm}

\newcommand{\@@C}[1]%
{\hfill{\makebox[\cmtlength][l]{\CommentFont{}#1\hfill}%
}}

\newcommand{\@@T}[1]%
{\textit{\uline{#1}}}

\newlength{\@@progwidth}
\newlength{\@@progwidthxx}
\newlength{\@@progheight}
\newlength{\@@progheightx}
\newlength{\@@progdepth}
\newsavebox{\@@wsProg}
\newenvironment{xprog}[1][\defcmtlength]
  %% Start def
  { \setlength{\cmtlength}{#1}
    \setlength{\@@progwidth}{\textwidth-(3cm)}
    \setlength{\@@progwidthxx}{\@@progwidth+4pt}
    \begin{lrbox}{\@@wsProg}%
    \begin{minipage}[t]{\@@progwidth}%
      \def\\{\char'134} %
      \def\|{\char'174} %
      \font\LocalProgramFont pcrr at 9pt %
      \begin{alltt}\baselineskip10pt\ProgramFont\obeylines}
  { \end{alltt}%
    \end{minipage}%
    \end{lrbox}%
    \vspace{0.3cm}%
      \settoheight{\@@progheight}{\usebox{\@@wsProg}}%
      \settodepth{\@@progdepth}{\usebox{\@@wsProg}}%
      \addtolength{\@@progheight}{\@@progdepth}%
      \addtolength{\@@progheight}{2pt}%
      \setlength{\@@progheightx}{\@@progheight-8.5pt}
      \hspace{0.8cm}%
      \rule[-\@@progheightx]{\sidebarwidth}{\@@progheight}%
      \hspace{0.6cm}%
      \parbox[t]{\@@progwidthxx}{\usebox{\@@wsProg}}%
    \vspace{0.3cm}}

  %% prog and inter environments, currently they do the same thing but they
  %% might get changed later.

  %% If someone can convince me auto line numbering is worth the effort, 
  %% I'll add it.
  
\newenvironment{program}[1][\defcmtlength] 
 {\let\C=\@@C %
  \begin{xprog}[#1]} 
 {\end{xprog}}

\newenvironment{interaction}[1][\defcmtlength]
 { \let\C=\@@C %
   \let\T=\@@T %
   \begin{xprog}[#1]}
 {\end{xprog}}


%% Sectioning commands

\renewcommand{\section}{\@startsection
  {section}%
  {1}%
  {0mm}%
  {\baselineskip}%
  {0.4\baselineskip}%
  {\large\sffamily\bfseries}}

\renewcommand{\subsection}{\@startsection
  {subsection}%
  {2}%
  {0mm}%
  {0.8\baselineskip}%
  {0.2\baselineskip}%
  {\sffamily\bfseries}}

\renewcommand{\subsubsection}{\@startsection
  {subsubsection}%
  {3}%
  {0mm}%
  {0.5\baselineskip}%
  {0.1\baselineskip}%
  {\normalsize\sffamily\slshape}}

\renewcommand{\@seccntformat}[1]{}

%% ----------------------------------------------------------------------
%% document environment changes

\AtBeginDocument{%
  %% Title generation commands
  %% Could improve multiline title handling
  \rule[0.7ex]{\textwidth}{0.4mm} \\ %
  \newsavebox{\@@titleA}%
  \sbox{\@@titleA}{{\LARGE\sffamily\bfseries \ws@short:\ }}%
  \newlength{\@@titleLength}%
  \newlength{\@@titleRem}%
  \settowidth{\@@titleLength}{\usebox{\@@titleA}}
  \setlength{\@@titleRem}{\textwidth-\@@titleLength}%
  \usebox{\@@titleA}%
  \parbox[t]{\@@titleRem}{{\raggedright\LARGE\sffamily\bfseries%
      \strut\ws@long\strut\par}}%
  \vspace{0cm} %  \vskip 1.3ex%
  \rule[0.2ex]{\textwidth}{0.4mm} \\%
  \makebox[\textwidth]{{\footnotesize \ws@author \hfill \ws@date}}%
  \vskip 8ex%
  \thispagestyle{empty}%
  }
\AtEndDocument{}

%% end of wsheet.cls
