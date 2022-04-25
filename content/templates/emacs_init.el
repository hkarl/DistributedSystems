(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(current-language-environment "UTF-8")
 '(org-latex-default-packages-alist
   '(("AUTO" "inputenc" t
      ("pdflatex"))
     ("T1" "fontenc" t
      ("pdflatex"))
     ("" "graphicx" t nil)
     ("" "grffile" t nil)
     ("" "longtable" nil nil)
     ("" "wrapfig" nil nil)
     ("" "rotating" nil nil)
     ("normalem" "ulem" t nil)
     ("" "amsmath" t nil)
     ("" "textcomp" t nil)
     ("" "amssymb" t nil)
     ("" "minted" t nil)
     ("" "capt-of" nil nil)
     ("" "xr-hyper" nil nil)
     ("" "hyperref" nil nil)))
 '(org-latex-hyperref-template nil)
 '(org-latex-prefer-user-labels t)
 '(org-latex-listings 'minted)
 '(org-beamer-environments-extra
   '(
     ("textbook" "T" "\\begin{textbook}" "\\end{textbook}")
     ("idea" "I" "\\begin{idea}" "\\end{idea}")
     ("requirement" "R" "\\begin{requirement}" "\\end{requirement}")
     ("observation" "O" "\\begin{observation}" "\\end{observation}")
     ("furtherreading" "L" "\\begin{furtherreading}" "\\end{furtherreading}")
     ))
 )

(with-eval-after-load 'ox-latex                                                                                   
  (add-to-list
   'org-latex-classes
   '("beamerhpi" "\\documentclass{beamerhpi}"
     ("\\section{%s}" . "\\section*{%s}")
     ("\\subsection{%s}" . "\\subsection*{%s}")
     ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
     ("\\paragraph{%s}" . "\\paragraph*{%s}")
     ("\\subparagraph{%s}" . "\\subparagraph*{%s}")
     )))

;; (add-to-list 'load-path (expand-file-name "~/.emacs.d/elpa/org-ref-20210506.1518"))
;; (add-to-list 'load-path (expand-file-name "~/.emacs.d/elpa/dash-20210210.1449"))
;; (add-to-list 'load-path (expand-file-name "~/.emacs.d/elpa/f-20191110.1357"))
;; (add-to-list 'load-path (expand-file-name "~/.emacs.d/elpa/s-20180406.808"))
;; (add-to-list 'load-path (expand-file-name "~/.emacs.d/elpa/htmlize-20200816.746"))
;; (add-to-list 'load-path (expand-file-name "~/.emacs.d/elpa/hydra-20201115.1055"))
;; (add-to-list 'load-path (expand-file-name "~/.emacs.d/elpa/lv-20200507.1518"))
;; (add-to-list 'load-path (expand-file-name "~/.emacs.d/elpa/parsebib-20210108.1525"))

(let ((default-directory  "~/.emacs.d/elpa/"))
  (normal-top-level-add-subdirs-to-load-path))

(require 'org-ref)
