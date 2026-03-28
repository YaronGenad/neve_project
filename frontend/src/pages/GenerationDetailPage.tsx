import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Grid from '@mui/material/Grid';
import Chip from '@mui/material/Chip';
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import CircularProgress from '@mui/material/CircularProgress';
import LinearProgress from '@mui/material/LinearProgress';
import Divider from '@mui/material/Divider';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Skeleton from '@mui/material/Skeleton';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DownloadIcon from '@mui/icons-material/Download';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import SchoolIcon from '@mui/icons-material/School';
import ClassIcon from '@mui/icons-material/Class';
import RepeatIcon from '@mui/icons-material/Repeat';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import RefreshIcon from '@mui/icons-material/Refresh';
import { getGeneration, downloadFile, submitGeneration } from '../api/generations';
import { approveMaterial, rejectMaterial, getMaterialVersions } from '../api/materials';
import { StatusChip } from '../components/StatusChip';
import { MaterialVersionItem } from '../types';

// File type definitions per round
interface FileDefinition {
  key: string;
  label: string;
  labelAr: string;
}

const GLOBAL_FILES: FileDefinition[] = [
  { key: 'student_pdf', label: 'PDF תלמיד', labelAr: 'PDF الطالب' },
  { key: 'teacher_pdf', label: 'PDF מורה', labelAr: 'PDF المعلم' },
];

const ROUND_FILES: FileDefinition[] = [
  { key: 'comprehension', label: 'הבנת הנקרא', labelAr: 'فهم القراءة' },
  { key: 'methods', label: 'שיטות', labelAr: 'أساليب' },
  { key: 'precision', label: 'דיוק', labelAr: 'دقة' },
  { key: 'vocabulary', label: 'אוצר מילים', labelAr: 'المفردات' },
  { key: 'student_pdf', label: 'PDF תלמיד', labelAr: 'PDF الطالب' },
  { key: 'teacher_pdf', label: 'PDF מורה', labelAr: 'PDF المعلم' },
  { key: 'answer_key', label: 'מפתח תשובות', labelAr: 'مفتاح الإجابات' },
  { key: 'teacher_prep', label: 'הכנת מורה', labelAr: 'تحضير المعلم' },
];

const formatDate = (iso?: string) => {
  if (!iso) return '—';
  try {
    return new Intl.DateTimeFormat('he-IL', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }).format(new Date(iso));
  } catch {
    return iso;
  }
};

interface DownloadButtonProps {
  generationId: string;
  fileType: string;
  label: string;
}

const DownloadButton: React.FC<DownloadButtonProps> = ({ generationId, fileType, label }) => {
  const [isDownloading, setIsDownloading] = useState(false);
  const [error, setError] = useState(false);

  const handleDownload = async () => {
    setIsDownloading(true);
    setError(false);
    try {
      await downloadFile(generationId, fileType);
    } catch {
      setError(true);
      setTimeout(() => setError(false), 3000);
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <Button
      variant={error ? 'outlined' : 'outlined'}
      color={error ? 'error' : 'primary'}
      size="small"
      onClick={handleDownload}
      disabled={isDownloading}
      startIcon={
        isDownloading ? <CircularProgress size={14} /> : <DownloadIcon fontSize="small" />
      }
      sx={{ minWidth: 140 }}
    >
      {error ? 'שגיאה / خطأ' : label}
    </Button>
  );
};

export const GenerationDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [approvalLoading, setApprovalLoading] = useState(false);
  const [toast, setToast] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success',
  });
  const [selectedVersionId, setSelectedVersionId] = useState<string | null>(null);

  const { data, isLoading, isError } = useQuery({
    queryKey: ['generation', id],
    queryFn: () => getGeneration(id!),
    enabled: !!id,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return status === 'pending' || status === 'processing' ? 5_000 : false;
    },
    staleTime: 2_000,
  });

  // Fetch versions when material data is available
  const { data: versionsData } = useQuery({
    queryKey: ['materialVersions', data?.subject, data?.topic, data?.grade],
    queryFn: () =>
      getMaterialVersions(data!.subject, data!.topic, data!.grade),
    enabled: !!(data?.status === 'completed' && data.subject && data.topic && data.grade),
    staleTime: 10_000,
  });

  const versions: MaterialVersionItem[] = versionsData?.versions ?? [];
  const effectiveMaterialId = selectedVersionId ?? data?.material_id ?? null;

  const showToast = (message: string, severity: 'success' | 'error') => {
    setToast({ open: true, message, severity });
  };

  const handleApprove = async () => {
    if (!effectiveMaterialId) return;
    setApprovalLoading(true);
    try {
      await approveMaterial(effectiveMaterialId);
      showToast('היחידה נשמרה ותוצג למורים נוספים ✓', 'success');
      queryClient.invalidateQueries({ queryKey: ['materialVersions'] });
    } catch {
      showToast('שגיאה בשמירה', 'error');
    } finally {
      setApprovalLoading(false);
    }
  };

  const handleReject = async () => {
    if (!effectiveMaterialId) return;
    setApprovalLoading(true);
    try {
      await rejectMaterial(effectiveMaterialId);
      // Re-generate with force_new=true
      const res = await submitGeneration({
        subject: data!.subject,
        topic: data!.topic,
        grade: data!.grade,
        rounds: data!.rounds,
        force_new: true,
      });
      navigate(`/generations/${res.generation_id}`);
    } catch {
      showToast('שגיאה ביצירת גרסה חדשה', 'error');
      setApprovalLoading(false);
    }
  };

  if (!id) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">מזהה לא תקין / معرف غير صالح</Alert>
      </Container>
    );
  }

  if (isError) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          שגיאה בטעינת הנתונים / خطأ في تحميل البيانات
        </Alert>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/dashboard')}>
          חזרה ללוח הבקרה / العودة للوحة التحكم
        </Button>
      </Container>
    );
  }

  const isActive = data?.status === 'pending' || data?.status === 'processing';
  const isCompleted = data?.status === 'completed';
  const isFailed = data?.status === 'failed';

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Back button */}
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/dashboard')}
        sx={{ mb: 3 }}
        color="inherit"
      >
        חזרה ללוח הבקרה / العودة للوحة التحكم
      </Button>

      {/* Header card */}
      <Card sx={{ mb: 3 }}>
        <CardContent sx={{ p: { xs: 3, sm: 4 } }}>
          {isLoading ? (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Skeleton variant="text" width="60%" height={40} />
              <Skeleton variant="text" width="40%" />
              <Skeleton variant="rectangular" width={120} height={32} sx={{ borderRadius: 4 }} />
            </Box>
          ) : (
            <>
              <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: 2, mb: 3 }}>
                <Box>
                  <Typography variant="h4" fontWeight={700} gutterBottom>
                    {data?.subject}
                  </Typography>
                  <Typography variant="h6" color="text.secondary">
                    {data?.topic}
                  </Typography>
                </Box>
                <StatusChip status={data?.status ?? 'pending'} size="medium" />
              </Box>

              {/* Metadata grid */}
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <ClassIcon color="primary" fontSize="small" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        כיתה / الصف
                      </Typography>
                      <Typography variant="body2" fontWeight={500}>
                        {data?.grade}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <RepeatIcon color="primary" fontSize="small" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        סבבים / الجولات
                      </Typography>
                      <Typography variant="body2" fontWeight={500}>
                        {data?.rounds}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box>
                    <Typography variant="caption" color="text.secondary">
                      נוצר ב / تاريخ الإنشاء
                    </Typography>
                    <Typography variant="body2" fontWeight={500}>
                      {formatDate(data?.created_at)}
                    </Typography>
                  </Box>
                </Grid>
                {data?.completed_at && (
                  <Grid item xs={6} sm={3}>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        הושלם ב / تاريخ الاكتمال
                      </Typography>
                      <Typography variant="body2" fontWeight={500}>
                        {formatDate(data.completed_at)}
                      </Typography>
                    </Box>
                  </Grid>
                )}
              </Grid>
            </>
          )}
        </CardContent>
      </Card>

      {/* Processing / pending state */}
      {isActive && (
        <Card sx={{ mb: 3 }}>
          <CardContent sx={{ p: 3, textAlign: 'center' }}>
            <CircularProgress size={48} sx={{ mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {data?.status === 'pending'
                ? 'ממתין לעיבוד... / في انتظار المعالجة...'
                : 'מעבד חומרי לימוד... / جارٍ معالجة المواد التعليمية...'}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              הדף יתעדכן אוטומטית כל 5 שניות / ستتحدث الصفحة تلقائياً كل 5 ثوانٍ
            </Typography>
            <LinearProgress color="primary" sx={{ borderRadius: 2, height: 6 }} />
          </CardContent>
        </Card>
      )}

      {/* Failed state */}
      {isFailed && (
        <Card sx={{ mb: 3, borderColor: 'error.main', borderWidth: 1, borderStyle: 'solid' }}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
              <ErrorOutlineIcon color="error" fontSize="large" />
              <Typography variant="h6" color="error">
                היצירה נכשלה / فشل الإنشاء
              </Typography>
            </Box>
            {data?.error && (
              <Typography
                variant="body2"
                sx={{
                  bgcolor: 'error.lighter',
                  p: 2,
                  borderRadius: 1,
                  fontFamily: 'monospace',
                  color: 'error.dark',
                  mt: 1,
                }}
              >
                {data.error}
              </Typography>
            )}
            <Button
              variant="contained"
              onClick={() => navigate('/generate')}
              sx={{ mt: 2 }}
            >
              נסה שוב / حاول مرة أخرى
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Completed — downloads */}
      {isCompleted && data && (
        <>
          {/* Approval action bar */}
          <Card sx={{ mb: 3, border: '2px solid', borderColor: 'primary.light' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                מה דעתך על היחידה? / ما رأيك في الوحدة؟
              </Typography>

              {/* Version selector (shown when multiple versions exist) */}
              {versions.length > 1 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    גרסאות קיימות / الإصدارات المتاحة:
                  </Typography>
                  <ToggleButtonGroup
                    value={effectiveMaterialId}
                    exclusive
                    onChange={(_, val) => val && setSelectedVersionId(val)}
                    size="small"
                  >
                    {versions.map((v) => (
                      <ToggleButton key={v.material_id} value={v.material_id}>
                        גרסה {v.version} ({v.approval_count} אישורים)
                      </ToggleButton>
                    ))}
                  </ToggleButtonGroup>
                </Box>
              )}

              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 1 }}>
                <Button
                  variant="contained"
                  color="success"
                  startIcon={
                    approvalLoading ? <CircularProgress size={16} color="inherit" /> : <CheckCircleOutlineIcon />
                  }
                  disabled={approvalLoading || !effectiveMaterialId}
                  onClick={handleApprove}
                >
                  ✓ מצוין, שמור / ممتاز، احفظ
                </Button>

                <Button
                  variant="outlined"
                  color="warning"
                  startIcon={
                    approvalLoading ? <CircularProgress size={16} color="inherit" /> : <RefreshIcon />
                  }
                  disabled={approvalLoading || !effectiveMaterialId}
                  onClick={handleReject}
                >
                  ↺ רוצה גרסה אחרת / أريد إصداراً آخر
                </Button>

                <Button
                  variant="text"
                  color="inherit"
                  startIcon={<DownloadIcon />}
                  disabled={approvalLoading}
                  onClick={() => data && downloadFile(data.generation_id, 'student_pdf')}
                >
                  ⬇ הורד בלי לאשר / تنزيل بدون موافقة
                </Button>
              </Box>
            </CardContent>
          </Card>

          {/* Global downloads */}
          <Card sx={{ mb: 3 }}>
            <CardHeader
              avatar={<MenuBookIcon color="primary" />}
              title={
                <Typography variant="h6" fontWeight={600}>
                  הורדות כלליות / تنزيلات عامة
                </Typography>
              }
            />
            <Divider />
            <CardContent>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                {GLOBAL_FILES.map((file) => (
                  <DownloadButton
                    key={file.key}
                    generationId={data.generation_id}
                    fileType={file.key}
                    label={`${file.label} / ${file.labelAr}`}
                  />
                ))}
              </Box>
            </CardContent>
          </Card>

          {/* Per-round downloads */}
          <Card>
            <CardHeader
              avatar={<SchoolIcon color="primary" />}
              title={
                <Typography variant="h6" fontWeight={600}>
                  הורדות לפי סבב / تنزيلات حسب الجولة
                </Typography>
              }
            />
            <Divider />
            <CardContent sx={{ pt: 2 }}>
              {Array.from({ length: data.rounds }, (_, i) => i + 1).map((round) => (
                <Accordion key={round} disableGutters elevation={0} sx={{ border: '1px solid', borderColor: 'divider', mb: 1, borderRadius: '8px !important', '&:before': { display: 'none' } }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip
                        label={`${round}`}
                        size="small"
                        color="primary"
                        sx={{ minWidth: 32 }}
                      />
                      <Typography fontWeight={500}>
                        סבב {round} / الجولة {round}
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1.5 }}>
                      {ROUND_FILES.map((file) => (
                        <DownloadButton
                          key={file.key}
                          generationId={data.generation_id}
                          fileType={`round${round}_${file.key}`}
                          label={`${file.label} / ${file.labelAr}`}
                        />
                      ))}
                    </Box>
                  </AccordionDetails>
                </Accordion>
              ))}
            </CardContent>
          </Card>

          {/* Result summary (if structured data available) */}
          {data.result && Object.keys(data.result).length > 0 && (
            <Card sx={{ mt: 3 }}>
              <CardHeader
                title={
                  <Typography variant="h6" fontWeight={600}>
                    סיכום תוצאות / ملخص النتائج
                  </Typography>
                }
              />
              <Divider />
              <CardContent>
                <Box
                  component="pre"
                  sx={{
                    bgcolor: 'grey.50',
                    p: 2,
                    borderRadius: 1,
                    overflow: 'auto',
                    fontSize: '0.8rem',
                    maxHeight: 400,
                    fontFamily: 'monospace',
                    direction: 'ltr',
                    textAlign: 'left',
                  }}
                >
                  {JSON.stringify(data.result, null, 2)}
                </Box>
              </CardContent>
            </Card>
          )}
        </>
      )}

      {/* Loading placeholders for downloads section */}
      {isLoading && (
        <Card>
          <CardContent sx={{ p: 3 }}>
            <Skeleton variant="text" width="30%" height={32} sx={{ mb: 2 }} />
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              {Array.from({ length: 4 }).map((_, i) => (
                <Skeleton key={i} variant="rectangular" width={150} height={36} sx={{ borderRadius: 1 }} />
              ))}
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Toast notification */}
      <Snackbar
        open={toast.open}
        autoHideDuration={4000}
        onClose={() => setToast((t) => ({ ...t, open: false }))}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          severity={toast.severity}
          onClose={() => setToast((t) => ({ ...t, open: false }))}
          sx={{ width: '100%' }}
        >
          {toast.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};
